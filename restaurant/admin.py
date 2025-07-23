from django.contrib import admin

from .models import (
    Article,
    CuisineType,
    Region,
    Restaurant,
    RestaurantCategory,
    RestaurantImage,
    RestaurantMenu,
    Review,
    ReviewImage,
    SocialChannel,
    Tag,
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # 관리자 목록 페이지에서 보여줄 컬럼을 지정함
    list_display = [  # 장고가 공식적으로 제공하는 admin 옵션 변수
        "id",
        "title",
        "show_at_index",
        "is_published",
        "created_at",
        "modified_at",
    ]

    # 개별 객체를 추가하거나 수정할 때 보여줄 필드를 지정함 (편집 화면에서 보임)
    # Admin에서 글을 생성하거나 수정할 때 이 필드들만 폼에 나타남
    fields = ["title", "preview_image", "content", "show_at_index", "is_published"]

    search_fields = ["title"]
    list_filter = ["show_at_index", "is_published"]
    date_hierarchy = "created_at"
    actions = ["make_published"]

    @admin.action(description="선택한 컬럼을 공개상태로 변경합니다.")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]
    search_fields = ["name"]


class RestaurantMenuInline(admin.TabularInline):
    model = RestaurantMenu
    extra = 1


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "branch_name",
        "is_closed",
        "phone",
        "rating",
        "rating_count",
        "region",
    ]
    fields = [
        "name",
        "branch_name",
        "category",
        "is_closed",
        "phone",
        "latitude",
        "longitude",
        "tags",
    ]
    readonly_fields = ["rating", "rating_count", "region"]
    search_fields = ["name", "branch_name"]
    list_filter = ["tags"]
    autocomplete_fields = ["tags"]
    inlines = [RestaurantMenuInline, RestaurantImageInline]  # 수정할때만 보여지는 폼

    # 수정할 때만 인라인 폼을 보여주고, 새로 생성할 때는 인라인 폼을 숨기는 역할
    def get_inline_instances(self, request, obj=None):
        return obj and super().get_inline_instances(request, obj) or []


@admin.register(RestaurantCategory)
class RestaurantCategoryIAdmin(admin.ModelAdmin):
    list_display = ["name"]
    fields = ["cuisine_type", "name"]


@admin.register(CuisineType)
class CuisineTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


# 이 클래스들은 InlineModelAdmin, 즉 인라인 모델 등록용 클래스입니다.
# RestaurantMenu는 Restaurant 객체를 수정할 때 같이 나타납니다.
# 왼쪽 메뉴에 "RestaurantMenu"라는 항목은 아예 없습니다.
# 대신, 레스토랑 수정 화면 안에 탭 형태로 들어가 있습니다.
class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "restaurant_name", "author", "rating", "content_partial"]
    inlines = [ReviewImageInline]

    # 인스턴스를 생성할때 인라인 표시 안하도록
    def get_inline_instances(self, request, obj=None):
        return obj and super().get_inline_instances(request, obj) or []


@admin.register(SocialChannel)
class SocialChannelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["name"]


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("sido", "sigungu", "eupmyeondong")
    search_fields = ("sido", "sigungu", "eupmyeondong")
