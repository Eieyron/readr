# for use with os.path.join
# fixes hardcoded path strings with /
# by splitting the string by these chars
# and letting os.path.join do the job
# str_path <- path string to be processed


def fix_path(str_path):
    # split by '/'
    res = str_path.split('/')

    return res
# res <- list to be used with os.path.join
# os.path.join('',*fix_path(str_path))
