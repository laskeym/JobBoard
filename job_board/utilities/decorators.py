from job_board import app

import pickle

def redisMemoize(func):
  """
  A memoization function based on a Redis cache.
  """
  def memoized_func(*args):
    if app.client.get(str(*args)):
      return pickle.loads(app.client.get(str(*args)))
    result = func(*args)
    app.client.set(str(*args), pickle.dumps(result), ex=3600)
    return result

  return memoized_func
