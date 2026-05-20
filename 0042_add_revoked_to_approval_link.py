from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from db.models import ApprovalLink, AuditLog

class ApprovalLinkRevokeView(APIView):
    def post(self, request, pk):
        try:
            approval_link = ApprovalLink.objects.get(pk=pk)
            if approval_link.revoked:
                return Response({'detail': 'Approval link already revoked'}, status=status.HTTP_400_BAD_REQUEST)
            if not approval_link.is_active():
                return Response({'detail': 'Cannot revoke inactive link'}, status=status.HTTP_400_BAD_REQUEST)

            approval_link.revoked = True
            approval_link.save()

            AuditLog.objects.create(
                actor=request.user,
                action='revoked',
                target_model='ApprovalLink',
                target_id=approval_link.id,
                timestamp=timezone.now()
            )

            return Response({'detail': 'Approval link revoked successfully'}, status=status.HTTP_200_OK)
        except ApprovalLink.DoesNotExist:
            return Response({'detail': 'Approval link not found'}, status=status.HTTP_404_NOT_FOUND)

class ApprovalLinkUIView(APIView):
    def get(self, request, pk):
        try:
            approval_link = ApprovalLink.objects.get(pk=pk)
            if approval_link.revoked:
                return Response({'detail': 'Approval link revoked'}, status=status.HTTP_410_GONE)
            if approval_link.is_expired():
                return Response({'detail': 'Approval link expired'}, status=status.HTTP_410_GONE)
            if approval_link.used:
                return Response({'detail': 'Approval link already used'}, status=status.HTTP_410_GONE)
            return Response({
                'detail': 'Approval link active',
                'status': 'active',
                'expires_at': approval_link.expires_at,
                'file': approval_link.file.name
            }, status=status.HTTP_200_OK)
        except ApprovalLink.DoesNotExist:
            return Response({'detail': 'Approval link not found'}, status=status.HTTP_404_NOT_FOUND)