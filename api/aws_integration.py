"""
FastAPI router for AWS account integration.
"""

from __future__ import annotations

from typing import Any

import boto3
from botocore.exceptions import ClientError
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, HttpUrl, validator

from ..models.aws_account import AwsAccount

__all__ = ["router"]

router = APIRouter(prefix="/aws", tags=["aws"])


class AddAwsAccountRequest(BaseModel):
    account_id: str
    role_arn: str
    name: str | None = None

    @validator("role_arn")
    def arn_must_be_valid(cls, v: str) -> str:
        if not v.startswith("arn:aws:iam::"):
            raise ValueError("role_arn must be a valid IAM role ARN")
        return v


class AddAwsAccountResponse(BaseModel):
    message: str
    account_id: str


def _assume_role_and_validate(role_arn: str) -> None:
    """
    Assume the supplied IAM role and perform a lightweight S3 list‑buckets call
    to confirm that the role has the required permissions.

    Raises HTTPException on any failure.
    """
    sts = boto3.client("sts")
    try:
        assumed = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName="axentx-integration-session",
            DurationSeconds=900,
        )
    except ClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to assume role: {exc.response['Error']['Message']}",
        ) from exc

    creds = assumed["Credentials"]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )
    try:
        s3.list_buckets()
    except ClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Assumed role lacks S3 permissions: {exc.response['Error']['Message']}",
        ) from exc


@router.post("/add", response_model=AddAwsAccountResponse)
def add_aws_account(req: AddAwsAccountRequest) -> AddAwsAccountResponse:
    """
    Add a new AWS account integration.

    1. Validate the IAM role ARN.
    2. Assume the role and perform a quick S3 permission check.
    3. Persist the account in the in‑memory store.
    """
    # 1 & 2 – validation
    _assume_role_and_validate(req.role_arn)

    # 3 – persistence
    try:
        account = AwsAccount.create(
            account_id=req.account_id,
            role_arn=req.role_arn,
            name=req.name or "",
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return AddAwsAccountResponse(
        message="AWS account successfully connected",
        account_id=account.account_id,
    )