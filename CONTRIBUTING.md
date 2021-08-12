# You can help contribute to Splunk OAR Response Templates

**DRAFT**

We are always on the lookout for new information to help refine and extend what is covered. If you have additional Incident Response techniques, know about variations on one already covered, or have other relevant information, then we would like to hear from you.

All contributions and feedback to Splunk OAR Response Templates are appreciated. Please don't hesitate to tell us what do you think could be improved by [submitting GitHub issue](#how-to-submit-an-issue).
# How to add a new Community playbook?
If you would like to contribute a Response Task only, you need to follow [How to add a new feature or create a pull request](#how-to-add-a-new-feature-or-create-a-pull-request) guideline, points 1, 2, 3, 5, 7, 8, bypassing 4 and 6, since you don't need the development environment.

# How to add a new Response or Response Task?

If you would like to contribute a Response Task only, you need to follow [How to add a new feature or create a pull request](#how-to-add-a-new-feature-or-create-a-pull-request) guideline, points 1, 2, 3, 5, 7, 8, bypassing 4 and 6, since you don't need the development environment.

Here is an example of good Response Task — [Indicator analysis](/workbooks/phases/tasks/indicator_analysis.yml) and a template for the fields below.

```
name: Name in sentence style
id: version 4 UUID
tags:
  - SOAR
  - PICERL
  - PHANTOM
  asset:
  - splunk
  - phantom_rest_api
  nist:
    RS.RP
description: description of the task for the analyst
input:
  - dest
  - userId
search: | tstats '...'
automation:
  role:
  sla_type: minutes
  sla:
  is_note_required: false
  actions:
    - actions needed
  playbooks:
    - scm:
      playook: <playbook you want to include
references:
how_to_implement: Explain it to me like I am 5
date: '2021-02-06'
version: 0
author: who made this
```
Please use the same approach for your contribution.  

# How to add a new Response content?

If you would like to contribute any response content, you need to fork the repo and then create a pull request with an issue describing what you are including what what it does.  We will follow up with more specific documentation on this to ensure all the content is centralized for everyone to get value from the content hosted here.

# How to submit an issue?

First, please refer to [contribution-guide.org](http://www.contribution-guide.org/) for the steps we expect from contributors before submitting an issue or bug report. Be as concrete as possible, include relevant logs, package versions etc.

The proper place for open-ended questions is you can request support at the #phantom-sme channel in Splunk internal Slack.

# How to add a new feature or create a pull request?

1. Fork the [ps-playbooks repository](https://github.com/splunk/ps-playbooks)
2. Clone your fork: `git clone https://github.com/<YOUR GITHUB USERNAME>/internal-oar-content.git`
3. Create a new branch based on `develop`: `git checkout -b <your github usernaem> develop`
4. Setup your Python enviroment
5. Implement your changes
6. Check your code for PEP8 requirements
7. Add files, commit and push: `git add ... ; git commit -m "my commit message"; git push origin my-feature`
8. [Create a PR](https://help.github.com/articles/creating-a-pull-request/) on Github. Write a **clear description** for your PR, including all the context and relevant information, such as:
   - The issue that you fixed, e.g. `Fixes #123`
   - Motivation: why did you create this PR? What functionality did you set out to improve? What was the problem + an overview of how you fixed it? Whom does it affect and how should people use it?
   - Any other useful information: links to other related Github or mailing list issues and discussions, benchmark graphs, academic papers…
   - Note that your Pull Request should be into the **develop** branch
