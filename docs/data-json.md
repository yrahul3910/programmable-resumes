# Data file (JSON)

A `data.json` file must be defined with the following spec. Note that dates must be in ISO-8601 format (YYYY-MM-DD). If you wish to denote the present, use null instead. Writers of templates must include checks to ensure that null dates are handled correctly.

```json
{
  "version": string,
  "personalInfo": {
    "name": string,
    "suffix": string?,
    "contact": {
      "email": string,
      "phone": string
    },
    "links": [{
      "display": string,
      "url": string
    }]
  },
  "summary": string,
  "education": [{
    "institution": string,
    "location": string,
    "degree": string,
    "dates": string[],
    "details": string[]?
  }],
  "employment": [{
    "organization": string,
    "location": string,
    "positions": [{
      "position": string,
      "dates": string[],
      "details": string[],
      "tags": string[]?
    }]
  }],
  "projects": [{
    "title": string,
    "dates": string[],
    "skills": string[],
    "links": [{
      "display": string,
      "url": string
    }]?,
    "details": string[],
    "tags": string[]?,
    "hidden": bool?
  }],
  "publications": string[],
  "talks": [{
    "title": string,
    "event": string,
    "date": string,
    "location": string
  }],
  "skills": [{
    "name": string,
    "type": string
  }],
  "honors": [{
    "date": string[] | string,
    "location": string?,
    "details": string?,
    "title": string,
    "hidden": boolean?
  }],
  "funding": [{
    "amount": string,
    "title": string,
    "date": string
  }],
  "service": [{
    "title": string,
    "details": string,
    "date": string?
  }]
}
```

## Tags

As an end-user, you can add _tags_ to your employment and projects. This is useful for creating multiple versions of your CVs, such as different roles that expect different kinds of projects. It's also useful for _hiding_ employment--for example, some people like having a "brag document" that lists individual accomplishments while they held a position, and usually summarize these points in their actual CV. You can use `data.json` as a brag document by creating a duplicate entry for the employment, and simply adding a `hidden` tag (note that the word "hidden" isn't special here, you can use anything as long as none of your configs actually set it to true). This lets you scroll a little bit to see individual accomplishments, and use that to write summarized bullet points for the visible version.

**Important:** Tags must be valid Python variables, so spaces or hyphens, for example, are not allowed.
