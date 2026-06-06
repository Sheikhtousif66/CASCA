import json
import os

MEM_FILE="memory.json"


# -----------------------------
# Default Long-Term Memory
# -----------------------------

def default_memory():

    return {

      "semantic_memory":{
  \
        "user":{

          "identity":{

             "name":"Sheikh Tousif",

             "degree":"MCA Student",

             "institution":
               "Assam Don Bosco University"
          },


          "goals":{

             "career":
                "Software Engineer",

             "project":
                "Build CASCA"
          },


          "preferences":{

             "communication_style":
                "Direct and practical"
          }

        },



        "casca":{

          "identity":{

             "name":"CASCA",

             "type":
               "Offline Personal AI Assistant",

             "personality":
               "Calm intelligent slightly witty"
          },


          "purpose":
            "Provide privacy preserving intelligent assistance.",



          "objectives":[

             "Develop offline AI assistant",

             "Enable voice interaction",

             "Provide contextual memory",

             "Ensure on-device privacy",

             "Support modular architecture"

          ],



          "architecture":{

             "input":
                "Speech and text",

             "reasoning":
                "Local language model",

             "memory":
                "Selective persistent memory",

             "output":
                "Voice synthesis",

             "emotion":
                "Emotion-aware responses"
          },



          "future_scope":[

             "Continual learning",

             "Graphical interface",

             "Advanced emotion recognition"

          ]
        }

      },



      "episodic_memory":[]
    }



# -----------------------------
# Load Memory
# -----------------------------

def load_memory():

    if not os.path.exists(MEM_FILE):

        mem=default_memory()

        with open(
            MEM_FILE,
            "w"
        ) as f:

            json.dump(
               mem,
               f,
               indent=2
            )

        return mem


    with open(
       MEM_FILE,
       "r"
    ) as f:

        return json.load(f)



# -----------------------------
# Save Memory
# -----------------------------

def save_memory(mem):

    with open(
       MEM_FILE,
       "w"
    ) as f:

        json.dump(
           mem,
           f,
           indent=2
        )



# -----------------------------
# Merge new episodic memory
# -----------------------------

def merge_new_memory(new_fact):

    if not new_fact:
        return


    mem=load_memory()


    mem["episodic_memory"].append(
       new_fact
    )


    # keep last 10 important events only
    mem["episodic_memory"]=(
      mem["episodic_memory"][-10:]
    )


    save_memory(mem)

def save_user_profile(about_me=None, ai_personality=None):

    mem = load_memory()

    if about_me is not None:
        mem["user_profile"]["about_me"] = about_me

    if ai_personality is not None:
        mem["user_profile"]["ai_personality"] = ai_personality

    save_memory(mem)



# -----------------------------
# Retrieval Context
# No routing logic
# Pure structured context
# -----------------------------

def retrieve_context():

    mem=load_memory()

    user=mem["semantic_memory"]["user"]

    casca=mem["semantic_memory"]["casca"]

    episodic=mem["episodic_memory"]


    context=f"""
USER PERSONAL MEMORY
(These are USER facts and goals,
not CASCA objectives)

{json.dumps(
 user,
 indent=2
)}


CASCA SELF KNOWLEDGE
(These belong to CASCA itself)

{json.dumps(
 casca,
 indent=2
)}


RECENT IMPORTANT EVENTS

{json.dumps(
 episodic,
 indent=2
)}
"""


    return context