# Demo Transcript

Live Q&A from `rag/demo.py` against the Acme Cloud help-center corpus.
Answers are extractive: synthesized from retrieved chunks, every claim cited.

## Q1: How much does the Growth plan cost per month?

**A:** Starter includes 1,000 build minutes/month and Growth includes 10,000. You can buy extra minutes at $0.005/min or upgrade your plan. Pay annually to save 20% on Growth seats. Scale contracts are annual by default. Growth is our most popular plan for production workloads. It includes 25 team seats, 1 TB of bandwidth per month, 10,000 build minutes per month, autoscaling, zero-downtime deploys, and email support with a 4-hour response time during business hours.

**Sources:**
- [1] Troubleshooting Common Errors > Out of build minutes (similarity 0.588)
- [2] Acme Cloud Pricing Plans > Annual billing (similarity 0.57)
- [3] Acme Cloud Pricing Plans > Growth — $29/month per seat (similarity 0.569)

## Q2: My deploy failed with a 502 Bad Gateway error. What should I check?

**A:** - `deploy.started` — a deployment began - `deploy.succeeded` — a deployment completed successfully - `deploy.failed` — a deployment failed (includes the build log excerpt) - `service.scaled` — autoscaling changed the replica count - `domain.verified` — a custom domain finished verification Cancel the deploy and retry. If it happens repeatedly, your build is likely downloading large dependencies on every run — add a build cache in **Service → Settings → Build Cache**, or split the build into smaller steps. Open the deploy log in the dashboard and look at the last 50 lines — the actual error is usually a missing dependency or a typo in the build command. The build command failed.

**Sources:**
- [1] Webhooks > Supported events (similarity 0.463)
- [2] Troubleshooting Common Errors > Deploy stuck in "Building" for over 20 minutes (similarity 0.423)
- [3] Troubleshooting Common Errors > Build failed: command exited with code 1 (similarity 0.414)

## Q3: How do I verify that a webhook payload is genuine?

**A:** Always verify this signature before trusting a payload. Every webhook request includes an `X-Acme-Signature` header: an HMAC-SHA256 of the raw request body, computed with your webhook signing secret. Go to **Project → Settings → Webhooks** and click **Add Webhook**. Enter the HTTPS URL that should receive events and select which events to subscribe to. Your endpoint must respond within 10 seconds with a 2xx status code. Failed deliveries appear in the webhook delivery log.

**Sources:**
- [1] Webhooks > Verifying signatures (similarity 0.738)
- [2] Webhooks > Creating a webhook (similarity 0.528)
- [3] Webhooks > Retries and timeouts (similarity 0.518)

## Q4: Is Acme Cloud SOC 2 certified, and how is my data encrypted?

**A:** Acme Cloud is SOC 2 Type II certified and ISO 27001 certified. Scale-plan customers can request our audit reports under NDA from the trust center at trust.acmecloud.example. Security is built into every layer of Acme Cloud. This page summarizes our certifications, encryption practices, and your responsibilities. All data is encrypted in transit with TLS 1.2 or higher, and at rest with AES-256. Database backups are encrypted with separate keys managed in a hardware security module (HSM).

**Sources:**
- [1] Security & Compliance > Certifications (similarity 0.735)
- [2] Security & Compliance > Overview (similarity 0.697)
- [3] Security & Compliance > Encryption (similarity 0.461)

## Q5: What happens if my payment method fails?

**A:** If payment fails after three retries, services are paused but your data is retained for 30 days. Update your payment method to resume immediately — no data is lost during the grace period. Add or update your card in **Billing → Payment Method**. We accept Visa, Mastercard, American Express, and ACH transfers (ACH on Growth and Scale only). How billing works on Acme Cloud: cycles, payment methods, invoices, and taxes.

**Sources:**
- [1] Billing & Invoices > Past-due accounts (similarity 0.604)
- [2] Billing & Invoices > Payment methods (similarity 0.492)
- [3] Billing & Invoices > Overview (similarity 0.337)
