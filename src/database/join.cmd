@echo off
type 010_user.sql > all.sql
type 020_subscription.sql >> all.sql
type 030_client.sql >> all.sql
type 040_professional.sql >> all.sql
type 050_address.sql >> all.sql
type 060_billing_type.sql >> all.sql
type 070_billing.sql >> all.sql
type 080_security_question.sql >> all.sql
type 090_user_question.sql >> all.sql
type 100_service.sql >> all.sql
type 110_associated_service.sql >> all.sql
type 120_authorisation.sql >> all.sql
type 130_session.sql >> all.sql
type 140_request_status.sql >> all.sql
type 150_request.sql >> all.sql
type 160_request_subscription.sql >> all.sql
type 170_request_transcation.sql >> all.sql