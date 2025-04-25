from .index_view import index_view
from .user_view import user_view
from .notice_view import notice_view
from .inquiry_view import inquiry_view

blueprints = [
    (index_view, "/"),          
    (user_view, "/"),       
    (notice_view, "/notice"),   
    (inquiry_view, "/inquiry"), 
]
