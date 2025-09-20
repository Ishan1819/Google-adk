from google.adk.agents import SequentialAgent
from .subagents.caption_generate.caption_generator import caption_generator_agent
from .subagents.insta_generate.instagram_poster import instagram_poster_agent

# Sequential pipeline
root_agent = SequentialAgent(
    name="InstaAutoPostPipeline",
    description="A pipeline that generates a caption and posts to Instagram",
    sub_agents=[caption_generator_agent, instagram_poster_agent],
)

# Make sure to expose the agent
__all__ = ["root_agent"]