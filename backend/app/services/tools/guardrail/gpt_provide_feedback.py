from services.clients.openai_client import GPTChatCompletionClient
from typing import Tuple, Union, Dict, Any
from config.keys import *
from models.gpt_feedback import GPT_SUMMARY_FEEDBACK
import json 
from config.logger import logger
example_summmary  = """
SpaceX: Avionics Hardware Engineer (Dragon) – Summary
Company Overview
Space Exploration Technologies Corp. (SpaceX) was founded in 2002 by Elon Musk, with headquarters in Hawthorne, California. Known for its reusable rocket technology, SpaceX has revolutionized the aerospace industry through Falcon 9 and Falcon Heavy launch vehicles, along with the Dragon spacecraft for ISS resupply and crew transport. Key leadership includes Elon Musk (CEO & Chief Engineer) and Gwynne Shotwell (President & COO).

Mission & Vision

Mission: “To revolutionize space technology, with the ultimate goal of enabling people to live on other planets.”
Vision: Develop cost-effective, reusable rockets and eventually establish a self-sustaining city on Mars.
Strategic Goals: Rapid innovation in launch technology, expansion of the Starlink satellite network, and pursuit of deep-space exploration with the Starship program.
Role Overview: Avionics Hardware Engineer (Dragon)

Core Focus: Designing, testing, and integrating avionics systems for the Dragon spacecraft.
Key Responsibilities:
Develop electrical assemblies, circuit boards, and test equipment.
Collaborate with multi-disciplinary teams (mechanical, software, manufacturing) to ensure reliable hardware performance in space environments.
Lead troubleshooting and root-cause investigations for hardware issues.
Optimize manufacturing processes and design for mission-critical flight hardware.
Required Skills & Qualifications

Minimum: Bachelor’s in Electrical/Computer Engineering (or related).
Technical Skills: PCB design (Altium/Orcad), system-level hardware debugging, analog/digital electronics.
Soft Skills: Strong problem-solving abilities, communication, ability to thrive in fast-paced environments.
Experience: Some roles may expect 1–5 years of relevant hardware experience, including internships or hands-on projects.
Interview Process

Prescreen: Initial phone or video discussion with a recruiter (focus on background/interest).
Technical Rounds: In-depth discussions with avionics teams, often involving circuit design challenges, test scenario walk-throughs, and system-level problem-solving.
Onsite or Final Rounds: A full-day series of interviews with engineers/managers; may include whiteboard sessions, design reviews, and cross-team Q&A about real-world hardware issues.
Salary & Benefits

Typical salary ranges (for mid-level): $100,000–$135,000 per year.
Equity & Bonuses: Stock options or performance-based bonuses are common.
Benefits Package: Comprehensive health coverage, 401(k) retirement plan, paid parental leave, and potential relocation assistance.
Career Growth

Promotion Path: Rapid advancement possible for high performers, given SpaceX’s growth and project diversity (e.g., transition from Dragon to Starlink or Starship teams).
Mentorship & Training: Primarily on-the-job learning with peer mentorship; formal training programs are less common but do exist.
Culture & Work-Life Balance

Fast-Paced Environment: Timelines are aggressive, and engineers often work extended hours during critical phases.
Innovative Mindset: Employees are encouraged to take initiative and solve problems creatively.
Employee Feedback: Glassdoor/Blind reviews note high engagement but also report demanding workloads.
References & Sources

Official Website: spacex.com/careers
Glassdoor: SpaceX Reviews
Levels.fyi: SpaceX Salaries

"""

def review_and_rate_output(initial_text: str) -> GPT_SUMMARY_FEEDBACK:
    prompt = f"""
You are a review agent. You have the following text to check for completeness and accuracy:
example good summary: {example_summmary}
=== BEGIN TEXT ===
{initial_text}
=== END TEXT ===

Please do the following:
Think of the review as offering a user enough context to prepare for a job interview. It cannot be based on vague, everything needs a source & you need to be strict, 
1. Decide if this text is good enough to continue or if it needs refinement. 
3. Output your decision and the revised or original text as **valid JSON** with the exact keys:
   "should_continue", "feedback", and "summary_rating".

**Important**:
- "should_continue" must be either true or false (no quotes). # if false agent will retry, give more falses than true
- "feedback" is a short string describing what's missing or confirming it's good.
- "summary_rating" a rating between 0-100
{{
    "should_continue": **boolean**,
    "feedback": **insert feedback from summary here*,
    "summary_rating": **insert rating of summary here 0-100 here**
}}
Return **no other text** outside the JSON.
"""
    messages = [
            {
                "role": "system", 
                "content": "You are a review agent. You have the following text to check for completeness and accuracy:", 
            },
            {
                "role": "user", 
                "content": f"the data is: {prompt}"
            }
        ]
    chat_client = GPTChatCompletionClient(base_url=ENDPOINT_OPENAI_GPT4, 
                                      api=OPENAI_GPT4_KEY,
                                      api_version=CHAT_VERSION,
                                      deployment_name=CHAT_DEPLOYMENT_NAME)
    response_format = {
            "type": "json_schema",
        "json_schema": {"name": "summary_feedback", "schema": GPT_SUMMARY_FEEDBACK.model_json_schema()}
    }
    response = chat_client.call(messages=messages, response_format=response_format)
    print(response)
    msgs = chat_client.parse_response(response)
    try: 
        # msg  =  string_to_json(msgs[-1])
        response = json.loads(msgs[-1])
    except Exception as e:
        logger.error("ERROR RESPONSE", e)
        raise SyntaxError("Response validation failed")
    print(msgs)
    return GPT_SUMMARY_FEEDBACK(**response)

def researcher_summary_feedback(result:str) -> Tuple[bool, Any] :
    feedback:GPT_SUMMARY_FEEDBACK = review_and_rate_output(result)

    if feedback.should_continue == False:
        return (False, str(feedback.model_dump()))
    return (True, {})