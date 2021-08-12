# You can help contribute to Splunk OAR Response Templates 

**DRAFT**

We are always on the lookout for new information to help refine and extend what is covered. If you have additional Incident Response techniques, know about variations on one already covered, or have other relevant information, then we would like to hear from you.

All contributions and feedback to Splunk OAR Response Templates are appreciated. Please don't hesitate to tell us what do you think could be improved by [submitting GitHub issue](#how-to-submit-an-issue).

# How to add a new Response Action?

If you would like to contribute a Response Task only, you need to follow [How to add a new feature or create a pull request](#how-to-add-a-new-feature-or-create-a-pull-request) guideline, points 1, 2, 3, 5, 7, 8, bypassing 4 and 6, since you don't need the development environment.

Here is an example of good Response Action — [3207: Block IP on IPS](response_actions/RA_3207_block_ip_on_ips.yml):

```
title: RA_3207_block_ip_on_ips
id: RA3207
description: Block an IP address in an IPS
author: '@atc_project'
creation_date: 31.01.2019
stage: containment
linked_analytics:
  - MS_IPS
workflow: |
  Block ip on IPS using native filtering functionality.
  Warning: 
  - If not all corporate hosts access the internet through the IPS, you will **not** be able to contain the threat using this Response Action.
  - Be careful blocking IP address. Make sure it's not a cloud provider or a hoster. If you would like to block something that is hosted on a well-known cloud provider or on a big hoster IP address, you should block a specific URL using alternative Response Action.
```

1. It is vendor-agnostic (doesn't include any specific IPS configurations)
2. It is detailed enough to be actionable and useful
3. Provides some important notes for a user

For now, we would like to focus on high-level definition of what should be done on a specific IR stage. It doesn't necessary to describe a specific way to configure IP blocking policy on a specific IPS solution (or any other system) since it is its basic functionality. If an organization has an IPS, we suppose that they know how to use it. If not, RE&CT will not (and doesn't suppose to) help.  

Please use the same approach for your contribution.  
