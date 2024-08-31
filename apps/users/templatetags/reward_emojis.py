from django import template

register = template.Library()


@register.filter
def reward_emojis(
    username: str,
    total_position: int,
) -> str:
    """Add emojis for first 3 users in context."""
    emojis = {
        1: "🏆",
        2: "🥈",
        3: "🥉",
    }
    return f"{username} {emojis.get(total_position)}"
