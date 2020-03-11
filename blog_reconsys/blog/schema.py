import graphene
from graphene_django.types import DjangoObjectType
from blog.models import Post, Comment
from graphql import GraphQLError


class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(object):
    post = graphene.Field(PostType, id=graphene.Int(), title=graphene.String(), description=graphene.String(),
                          publish_date=graphene.Date(), author=graphene.String())
    posts = graphene.List(PostType)

    comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.Int(), text=graphene.String(), author=graphene.String())

    def resolve_posts(self, info, **kwargs):
        """
        Fetches all the posts
        """
        return Post.objects.all()

    def resolve_comments(self, info, **kwargs):
        """
        Fetches all comments
        """
        return Comment.objects.select_related('post').all()

    def resolve_post(self, info, **kwargs):
        """
        Fetch single Post object based on Id
        """
        id = kwargs.get('id')

        if id is not None:
            return Post.objects.get(pk=id)

        return None

    def resolve_comment(self, info, **kwargs):
        """
        Fetches single Comment object based on Id
        """
        id = kwargs.get('id')

        if id is not None:
            return Comment.objects.get(pk=id)

        return None


class PostMixin(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        author = graphene.String(required=True)

    post = graphene.Field(PostType)

    class Meta:
        abstract = True


class CreatePost(PostMixin):
    def mutate(self, info, title, description, author):
        post_obj = Post.objects.create(title=title, description=description, author=author)
        return CreatePost(post=post_obj)


class UpdatePost(PostMixin):
    def mutate(self, info, id, title, description, author):
        # TODO: Exception handling
        post_obj = Post.objects.get(pk=id)
        post_obj.title = title
        post_obj.description = description
        post_obj.author = author
        post_obj.save()

        return UpdatePost(post=post_obj)


class CommentMixin(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=False)
        postId = graphene.Int(required=False)
        text = graphene.String(required=True)
        author = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    class Meta:
        abstract = True


class CreateComment(CommentMixin):

    def mutate(self, info, postId, text, author, id=None):
        try:
            post_obj = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            raise GraphQLError('Please Enter a valid postId')

        comment_obj = Comment.objects.create(post=post_obj, text=text, author=author)
        return CreateComment(comment=comment_obj)


class UpdateComment(CommentMixin):
    def mutate(self, info, id, text, author):
        comment_obj = Comment.objects.get(pk=id)
        comment_obj.text = text
        comment_obj.author = author
        comment_obj.save()
        return UpdateComment(comment=comment_obj)


class Mutation(graphene.ObjectType):
    createPost = CreatePost.Field()
    updatePost = UpdatePost.Field()
    createComment = CreateComment.Field()
    updateComment = UpdateComment.Field()
