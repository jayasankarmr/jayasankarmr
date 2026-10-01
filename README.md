<div align="center">

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg" /><img src="assets/hero-light.svg" width="100%" alt="Jayasankar M R. Cloud &amp; DevOps Engineer · Final-Year CSE Student. Making systems faster, cheaper, and more reliable." /></picture>

<a href="https://www.linkedin.com/in/jayasankar-m-r-1483802a5"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/link-linkedin-dark.svg" /><img src="assets/link-linkedin-light.svg" width="32%" alt="LinkedIn" /></picture></a>
<a href="mailto:jayasankar.mr7@gmail.com"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/link-email-dark.svg" /><img src="assets/link-email-light.svg" width="32%" alt="Email: jayasankar.mr7@gmail.com" /></picture></a>
<a href="https://www.credly.com/users/jayasankar-m-r.eede608c"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/link-credly-dark.svg" /><img src="assets/link-credly-light.svg" width="32%" alt="Credly" /></picture></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/status-dark.svg" /><img src="assets/status-light.svg" width="100%" alt="Open to: Internship | 2027 Full-time · Location: Delhi-NCR, open to relocate Pan-India · B.Tech CSE, Class of 2027" /></picture>

</div>

<br />

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-01-flagship-dark.svg" /><img src="assets/hdr-01-flagship-light.svg" width="100%" alt="01 Flagship project" /></picture>

### [warm-pool-governor](https://github.com/jayasankarmr/warm-pool-governor)
**Resizes an EC2 Auto Scaling warm pool from live CPU. AWS only lets you size it once, by hand.**

<a href="https://github.com/jayasankarmr/warm-pool-governor"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg" /><img src="assets/stats-light.svg" width="100%" alt="63.8% projected cost saving vs always-on · 2m43s sooner than a CPU alarm · O(1) pure decision, no forecast · 604 tests, run fully offline" /></picture></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/governor-dark.svg" /><img src="assets/governor-light.svg" width="100%" alt="Control loop: EventBridge triggers a Lambda every minute; it reads CPU from CloudWatch, picks COST_SAVING (under 20%), PRE_WARM (20–40%) or MITIGATE (40% and up), and writes the warm pool size to the Auto Scaling group only when it changes." /></picture>

- Every native scaling policy only moves `DesiredCapacity`. This moves the warm pool's own bounds, so standby capacity exists while load needs it and drains to zero when it doesn't.
- In steady state each tick is **two reads, zero writes**. Writes are ordered so every intermediate state stays valid.
- Missing metric data is treated as unknown, not as 0%, so a broken monitoring pipeline can't drain the pool mid-spike.
- Terraform deploys both the baseline and the governor, with **five IAM actions** scoped to one group. CI runs `tflint` and `checkov`.

`Python` · `Boto3` · `Lambda` · `EC2 Auto Scaling` · `CloudWatch` · `EventBridge` · `Terraform` · `GitHub Actions` · [**Repository →**](https://github.com/jayasankarmr/warm-pool-governor)

<br />

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-02-about-dark.svg" /><img src="assets/hdr-02-about-light.svg" width="100%" alt="02 About" /></picture>

Final-year B.Tech Computer Science student at **SRM Institute of Science and Technology, Delhi-NCR** (**CGPA 9.35/10**) and an **AWS Certified Cloud Practitioner** who builds and automates cloud infrastructure.

I like problems where the win is measurable, and I've shipped to production outside coursework: six months owning DNS, secure routing, release and incident response for two live client platforms during an industry internship.

```text
now  working toward AWS Solutions Architect – Associate (Dec 2026)
     learning Terraform and Kubernetes
     open to internships and 2027 new-grad roles
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/about-dark.svg" /><img src="assets/about-light.svg" width="100%" alt="9.35 CGPA out of 10 at SRM IST, Delhi-NCR · 6 months of production ops in an industry internship · 2 live client platforms: DNS, routing, release · AWS Certified Cloud Practitioner" /></picture>

<br />

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-03-experience-dark.svg" /><img src="assets/hdr-03-experience-light.svg" width="100%" alt="03 Experience" /></picture>

<table>
<tr>
<td width="120" valign="top"><code>2025-06 →</code><br /><code>2025-12</code></td>
<td valign="top">

**Systems and Integrations Developer Intern → Trainee**<br />
<sub>GeToday Global Limited, London (Remote)</sub>

- Owned the provisioning and production release lifecycle for **two live client platforms** end to end: DNS records, secure routing, SSL/TLS and environment configuration, taking each to live traffic.
- Ran post-release operations with minimal supervision: monitored platform health, triaged incidents, traced faults to root cause and verified fixes on **revenue-generating systems**.
- Built REST API integrations feeding third-party catalogues into core infrastructure, automating revenue-split and payment-gateway workflows. **Promoted to Trainee within the term.**

</td>
</tr>
<tr>
<td width="120" valign="top"><code>2025</code></td>
<td valign="top">

**AI-Powered Cloud Engineer Virtual Intern**<br />
<sub>AWS &amp; AICTE</sub>

- Hands-on AWS labs in cloud architecture and infrastructure management, applying least-privilege IAM, monitoring and cost controls.

</td>
</tr>
</table>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-04-certifications-dark.svg" /><img src="assets/hdr-04-certifications-light.svg" width="100%" alt="04 Certifications" /></picture>

<!-- Between the credly markers is generated by .github/workflows/credly.yml from the
     public Credly profile. Edit .github/scripts/credly.py, not this block. -->
<!--START_SECTION:credly-->
<table>
<tr>
<td align="center" width="130">
<a href="https://www.credly.com/badges/7d2823e1-296d-4fbc-b71e-0c4e117b706b">
<img src="https://images.credly.com/size/340x340/images/00634f82-b07f-4bbd-a6bb-53de397fc3a6/image.png" width="95" alt="AWS Certified Cloud Practitioner" />
</a>
</td>
<td>

**AWS Certified Cloud Practitioner**
`EARNED Jun 2026` · valid to Jun 2029 · Amazon Web Services

[Verify on Credly →](https://www.credly.com/badges/7d2823e1-296d-4fbc-b71e-0c4e117b706b)

</td>
<td align="center" width="130">
<img src="https://images.credly.com/size/340x340/images/0e284c3f-5164-4b21-8660-0d84737941bc/image.png" width="95" alt="AWS Certified Solutions Architect – Associate" />
</td>
<td>

**AWS Certified Solutions Architect – Associate**
`IN PROGRESS` · targeting Dec 2026

</td>
</tr>
</table>

**Training badges** <sub>(10 · hover for names)</sub>

<a href="https://www.credly.com/badges/80728662-f747-4dd4-aa2d-9a89366c8b36"><img src="https://images.credly.com/size/110x110/images/e50c657a-edd9-4c93-b1cf-2b6634b54abf/blob" width="52" alt="AWS Educate Introduction to Generative AI - Training Badge" title="AWS Educate Introduction to Generative AI - Training Badge" /></a> <a href="https://www.credly.com/badges/ad9d3712-4b46-4f90-a958-ea0389315d6d"><img src="https://images.credly.com/size/110x110/images/247efe36-9fa6-4209-ad56-0fd522283872/blob" width="52" alt="AWS Educate Machine Learning Foundations - Training Badge" title="AWS Educate Machine Learning Foundations - Training Badge" /></a> <a href="https://www.credly.com/badges/c5e59b6c-96f9-4910-828c-0e68e4575280"><img src="https://images.credly.com/size/110x110/images/25108813-2dd7-45f7-8158-65689b8526b5/blob" width="52" alt="AWS Educate Getting Started with Serverless - Training Badge" title="AWS Educate Getting Started with Serverless - Training Badge" /></a> <a href="https://www.credly.com/badges/26c76833-a4e0-4e68-83c2-8437cf4473d1"><img src="https://images.credly.com/size/110x110/images/4251ab91-6d67-47da-801c-855c0bbc6cc3/blob" width="52" alt="AWS Educate Getting Started with Cloud Ops - Training Badge" title="AWS Educate Getting Started with Cloud Ops - Training Badge" /></a> <a href="https://www.credly.com/badges/10f20ec4-271a-4059-a18a-494fbafef2e0"><img src="https://images.credly.com/size/110x110/images/a08cf90b-9838-4f6c-82bd-8db85fb89dd5/blob" width="52" alt="AWS Educate Getting Started with Databases - Training Badge" title="AWS Educate Getting Started with Databases - Training Badge" /></a> <a href="https://www.credly.com/badges/2e227766-3789-4585-85be-6590a511000c"><img src="https://images.credly.com/size/110x110/images/f5095707-7683-4886-940c-3e8e4a2085ca/blob" width="52" alt="AWS Educate Getting Started with Networking - Training Badge" title="AWS Educate Getting Started with Networking - Training Badge" /></a> <a href="https://www.credly.com/badges/dd615cc3-dfcf-406e-992e-8a87e651cbb4"><img src="https://images.credly.com/size/110x110/images/fc6fa322-80f4-45a5-9def-91e9bcfde837/blob" width="52" alt="AWS Educate Getting Started with Security - Training Badge" title="AWS Educate Getting Started with Security - Training Badge" /></a> <a href="https://www.credly.com/badges/7bf6bd1c-1ab8-465d-9cad-52c7dce28e17"><img src="https://images.credly.com/size/110x110/images/7b08cc0e-064b-407d-b70e-323509c3e474/blob" width="52" alt="AWS Educate Getting Started with Compute - Training Badge" title="AWS Educate Getting Started with Compute - Training Badge" /></a> <a href="https://www.credly.com/badges/24da4581-3fd6-47dd-895f-fb75b07d8d9d"><img src="https://images.credly.com/size/110x110/images/3b1b42e6-dfc2-492b-90df-8058096cb93d/blob" width="52" alt="AWS Educate Getting Started with Storage - Training Badge" title="AWS Educate Getting Started with Storage - Training Badge" /></a> <a href="https://www.credly.com/badges/b0393431-408d-4398-900b-c06c8135f38d"><img src="https://images.credly.com/size/110x110/images/e51a8579-188d-4363-8ed1-12ad164ef57b/blob" width="52" alt="AWS Educate Introduction to Cloud 101 - Training Badge" title="AWS Educate Introduction to Cloud 101 - Training Badge" /></a>
<!--END_SECTION:credly-->

Also: **The Bits and Bytes of Computer Networking** · Google (Coursera) · [all badges on Credly →](https://www.credly.com/users/jayasankar-m-r.eede608c)

<br />

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-05-projects-dark.svg" /><img src="assets/hdr-05-projects-light.svg" width="100%" alt="05 More projects" /></picture>

<table>
<tr>
<td width="33%" valign="top">
<a href="https://github.com/jayasankarmr/LifeDrop"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-lifedrop-dark.svg" /><img src="assets/project-lifedrop-light.svg" width="100%" alt="LifeDrop: Blood bank management system. Multi-role app connecting donors, hospitals and admins. Low-stock alerts, rate limiting, CSRF protection, CSP. Built with Flask, SQLAlchemy, SQLite, Tailwind." /></picture></a>
<sub><a href="https://lifedrop-demo.onrender.com/">Live demo →</a> · <a href="https://github.com/jayasankarmr/LifeDrop">Repo</a></sub>
</td>
<td width="33%" valign="top">
<a href="https://github.com/jayasankarmr/Downright"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-downright-dark.svg" /><img src="assets/project-downright-light.svg" width="100%" alt="Downright: Chrome / Edge extension. Copy any page as clean Markdown in one keystroke, with correct tables, code fences and math. No tracking, no network. Built with JavaScript, Chrome Extension API." /></picture></a>
<sub><a href="https://github.com/jayasankarmr/Downright">Repo →</a></sub>
</td>
<td width="33%" valign="top">
<a href="https://github.com/jayasankarmr/credit-risk-analyser"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/project-credit-risk-dark.svg" /><img src="assets/project-credit-risk-light.svg" width="100%" alt="Credit Risk Analyser: Default-risk modelling. End-to-end credit default risk pipeline: feature engineering on borrower and loan attributes, model comparison and evaluation. Built with scikit-learn, Pandas, Jupyter." /></picture></a>
<sub><a href="https://github.com/jayasankarmr/credit-risk-analyser">Repo →</a></sub>
</td>
</tr>
</table>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-06-stack-dark.svg" /><img src="assets/hdr-06-stack-light.svg" width="100%" alt="06 Stack" /></picture>

```text
cloud    AWS (EC2 · Auto Scaling · Lambda · CloudWatch · IAM · VPC · S3 · RDS) · Azure · GCP
code     Python · Boto3 · Bash · Linux · SQL · C++ · JavaScript · TypeScript
devops   Docker · GitHub Actions · Git · CI/CD · Agile/Scrum
observe  CloudWatch metrics, alarms & dashboards · log analysis · incident triage · RCA
network  TCP/IP · DNS · HTTP/S · SSL/TLS · load balancing · IAM/RBAC · least privilege
data     PostgreSQL · MySQL · SQLite · MongoDB · Flask · Node.js
learning Terraform · Kubernetes (coursework and self-study)
```

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-07-activity-dark.svg" /><img src="assets/hdr-07-activity-light.svg" width="100%" alt="07 Activity" /></picture>

<!-- assets/activity-*.svg is generated daily by .github/workflows/activity.yml. -->
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg" /><img src="assets/activity-light.svg" width="100%" alt="GitHub contributions over the last year, current and longest streak, and languages by bytes across my repositories" /></picture>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/hdr-08-beyond-dark.svg" /><img src="assets/hdr-08-beyond-light.svg" width="100%" alt="08 Beyond code" /></picture>

**Vice Chairperson, ACM, SRM Student Chapter** · `Aug 2025 – Present`<br />
Led a cross-functional team through the full delivery lifecycle of *Visualize It*, a data competition for **40+ participants**.

**Rajya Puraskar Awardee** · The Bharat Scouts and Guides<br />
State-level award for leadership and community service.

**Photography** · where I go when I'm not in a terminal

<a href="https://jayasankarmr.github.io/Photography-Portfolio/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/frame-tower-dark.svg" /><img src="assets/frame-tower-light.svg" width="32%" alt="Frame 01, tower: telecom tower silhouetted against a setting sun" /></picture></a>
<a href="https://jayasankarmr.github.io/Photography-Portfolio/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/frame-peacock-dark.svg" /><img src="assets/frame-peacock-light.svg" width="32%" alt="Frame 02, peacock: peacock in dappled forest light" /></picture></a>
<a href="https://jayasankarmr.github.io/Photography-Portfolio/"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/frame-cupola-dark.svg" /><img src="assets/frame-cupola-light.svg" width="32%" alt="Frame 03, cupola: black-and-white carved stone cupola" /></picture></a>

<sub>[Full portfolio →](https://jayasankarmr.github.io/Photography-Portfolio/)</sub>

<br />

<div align="center">

**Best way to reach me:** [jayasankar.mr7@gmail.com](mailto:jayasankar.mr7@gmail.com) · I reply within a day.

</div>
