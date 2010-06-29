from django.conf import settings

# Used to limit the number of unique IPs that can vote on a single object+field.
#   useful if you're getting rating spam by users registering multiple accounts
RATINGS_VOTES_PER_IP = 3

# Karel Stastny - number of anonymous ratings allowed from one IP
ANONYMOUS_RATINGS_VOTES_PER_IP = 5
