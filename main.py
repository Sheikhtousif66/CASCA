from brain import generate_response, extract_memory
from memory import merge_new_memory
from voice import speak
from stt import listen


print("\nCASCA initialized.\n")
print("CASCA: Casca Online.")


def run_casca(user, audio_stats=None, speak_enabled=True):

    if not user:
        return {
            "response": "Say something."
        }

    response = generate_response(
        user,
        audio_stats
    )

    if speak_enabled:

        try:
            speak(response)

        except Exception:
            pass

    try:

        fact = extract_memory(
            user,
            response
        )

        merge_new_memory(
            fact
        )

    except Exception:
        pass

    return {
        "response": response
    }



if __name__ == "__main__":

    try:

        speak(
            "Hello there boss what's on your mind today"
        )

    except Exception:

        pass


    while True:

        user = input(
            "\nType message (or V for voice): "
        ).strip()

        audio_stats = None

        if user.lower() == "v":

            user, audio_stats = listen()

        if not user:
            continue

        if user.lower() in [
            "exit",
            "quit"
        ]:
            break

        result = run_casca(
            user,
            audio_stats
        )

        print(
            "\nCASCA:",
            result["response"]
        )