import importlib


def test_log_queries():
    print("\n=== Test: log_queries ===")
    log_queries_module = importlib.import_module('0-log_queries')
    fetch_all_users = log_queries_module.fetch_all_users
    users = fetch_all_users("SELECT * FROM users")
    print("Fetched users:", users)


def test_with_db_connection():
    print("\n=== Test: with_db_connection ===")
    with_db_connection_module = importlib.import_module('1-with_db_connection')
    get_user_by_id = with_db_connection_module.get_user_by_id
    user = get_user_by_id(user_id=1)
    print("Fetched user with ID 1:", user)


def test_transactional():
    print("\n=== Test: transactional ===")
    transactional_module = importlib.import_module('2-transactional')
    update_user_email = transactional_module.update_user_email
    update_user_email(user_id=1, new_email='new_email@example.com')
    print("User email updated successfully.")


def test_retry_on_failure():
    print("\n=== Test: retry_on_failure ===")
    retry_module = importlib.import_module('3-retry_on_failure')
    fetch_users_with_retry = retry_module.fetch_users_with_retry
    users = fetch_users_with_retry()
    print("Fetched users with retry:", users)


def test_cache_query():
    print("\n=== Test: cache_query ===")
    cache_module = importlib.import_module('4-cache_query')
    fetch_users_with_cache = cache_module.fetch_users_with_cache
    # First call - should be a cache miss
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print("First fetch:", users)
    # Second call - should be a cache hit
    users_cached = fetch_users_with_cache(query="SELECT * FROM users")
    print("Second fetch (from cache):", users_cached)


if __name__ == "__main__":
    test_log_queries()
    test_with_db_connection()
    test_transactional()
    test_retry_on_failure()
    test_cache_query()
