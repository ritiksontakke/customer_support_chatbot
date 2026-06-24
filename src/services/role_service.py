from src.config.database import supabase
def get_user_role(user_id: str):

    result = (
        supabase.table("users")
        .select("roles(name)")
        .eq("id", user_id)
        .single()
        .execute()
    )

    return result.data["roles"]["name"]