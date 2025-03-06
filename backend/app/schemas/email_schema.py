
email_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GPT_Email_Summary_Response",
  "type": "object",
  "properties": {
    "summary": {
      "type": "string"
    },
    "company": {
      "type": "string"
    },
    "job_position": {
      "type": "string"
    }
  },
  "required": ["summary", "company", "job_position"]
}