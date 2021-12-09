-- upgrade --
ALTER TABLE "post" ALTER COLUMN "logged_only" DROP DEFAULT;
-- downgrade --
ALTER TABLE "post" ALTER COLUMN "logged_only" SET DEFAULT False;
