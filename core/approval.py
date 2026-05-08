APPROVAL_WORDS = {
    "yes",
    "ok",
    "okay",
    "go ahead",
    "proceed",
    "approved"
}


def is_approved(user_input):

    cleaned = user_input.lower().strip()

    return cleaned in APPROVAL_WORDS