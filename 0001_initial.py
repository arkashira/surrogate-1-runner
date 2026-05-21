BEGIN;

CREATE TABLE "investors_investor" (
    "id" serial PRIMARY KEY,
    "email" varchar(254) NOT NULL UNIQUE,
    "password" varchar(128) NOT NULL,
    "two_factor_secret" varchar(16) NULL,
    "firm_name" varchar(200) NOT NULL,
    "investment_stage" varchar(20) NOT NULL,
    "ticket_size" numeric(12,2) NOT NULL,
    "focus_areas" jsonb NOT NULL DEFAULT '[]',
    "geographic_preference" jsonb NOT NULL DEFAULT '[]',
    "created_at" timestamptz NOT NULL DEFAULT now(),
    "updated_at" timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX "investors_investor_email_idx" ON "investors_investor" ("email");
CREATE INDEX "investors_investor_firm_name_idx" ON "investors_investor" ("firm_name");
CREATE INDEX "investors_investor_investment_stage_idx" ON "investors_investor" ("investment_stage");
CREATE INDEX "investors_investor_ticket_size_idx" ON "investors_investor" ("ticket_size");

COMMIT;