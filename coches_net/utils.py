# an ad-hoc exception to raise if some of the ad pages have not been processed
class AdNotProcessedException(Exception):
    def __init__():
        exception_msg = \
        ('A problem has ocurred when extracting one of the'
         'dataframes. stopping execution')
        super().__init__(exception_msg)
