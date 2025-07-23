from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError


class Article(models.Model):
    title = models.CharField(max_length=100, db_index=True)  # 검색 속도 향상
    preview_image = models.ImageField(upload_to="article", null=True, blank=True)
    # 업로드된 이미지는 /media/article/ 폴더 안에 저장됨.

    content = models.TextField()
    show_at_index = models.BooleanField(
        default=False
    )  # 기본값은 False (즉, 체크 안 된 상태로 저장됨).
    is_published = models.BooleanField(
        default=False
    )  # 기본값은 False (즉, 체크 안 된 상태로 저장됨).
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True
    )  # 객체가 처음 생성될 때만 현재 시각으로 자동 저장.
    modified_at = models.DateTimeField(
        auto_now=True
    )  # 객체가 수정될 때마다 자동으로 시간 업데이트됨.

    class Meta:
        verbose_name = "칼럼"
        verbose_name_plural = "칼럼"  # 푸얼러

    def __str__(self):
        return f"{self.id} - {self.title}"


class Restaurant(models.Model):
    name = models.CharField("이름", max_length=100, db_index=True)
    branch_name = models.CharField(
        "지점", max_length=100, db_index=True, null=True, blank=True
    )
    description = models.TextField("설명", null=True, blank=True)
    address = models.CharField("주소", max_length=255, db_index=True)
    feature = models.CharField("특징", max_length=255)
    is_closed = models.BooleanField("폐업 여부", default=False)
    latitude = models.DecimalField(  # 고정 소수점 숫자를 저장하는 필드. 위도/경도와 같은 정밀한 실수 표현에 적합.
        "위도",
        max_digits=16,  # 전체 숫자 자릿수 (소수점 포함 총 16자리까지 허용).
        decimal_places=12,  # 소수점 이하 자릿수 (정수부는 4자리, 소수부는 12자리 허용).
        db_index=True,  # 검색 최적화를 위해 인덱스 생성.
        default="0.0000",  # 기본값 설정. 문자열로 설정되어 있지만 숫자로 변환되어 저장됨.
    )
    longitude = models.DecimalField(
        "경도",
        max_digits=16,
        decimal_places=12,
        db_index=True,
        default="0.0000",
    )
    phone = models.CharField(
        "전화번호", max_length=16, help_text="E.164 포맷", blank=True, null=True
    )
    rating = models.DecimalField(
        "평점", max_digits=3, decimal_places=2, default="0.0"
    )  # 예: 9.99까지 가능 (최대 소수점 둘째 자리까지 표현됨).
    rating_count = models.PositiveIntegerField(
        "평가수", default=0
    )  # 0 이상의 양의 정수만 허용하는 필드 (예:좋아요 수, 평가 수 등).
    start_time = models.TimeField(
        "영업 시작 시간", null=True, blank=True
    )  # 시/분/초 단위의 시간만 저장하는 필드 (날짜는 없음). 예: 18:30:00
    end_time = models.TimeField("영업 종료 시간", null=True, blank=True)
    last_order_time = models.TimeField("라스트 오더 시간", null=True, blank=True)
    category = models.ForeignKey(
        "RestaurantCategory",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,  # 참조된 카테고리 삭제 시, 이 필드 값을 NULL로 설정 (데이터 보존).
    )
    tags = models.ManyToManyField(
        "Tag", blank=True
    )  # 다대다(M:N) 관계 설정. 하나의 레스토랑이 여러 태그를 가질 수 있음.
    region = models.ForeignKey(
        "Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="지역",  # 관리자 페이지 필드명 한국어로 표시됨.
        related_name="restaurants",  # 역참조 시 사용. 예: region.restaurants.all()로 해당 지역의 모든 레스토랑 조회 가능.
        # Restaurant → Region
        # → 레스토랑은 "한" 지역에 속합니다 (지역을 참조합니다).
        # Region ← Restaurant
        # → 하나의 지역은 여러 개의 레스토랑이 있을 수 있습니다.
        # → 이때 지역에서 연결된 레스토랑들을 찾아오는 방법이 바로 .restaurants 입니다.
        # restaurant.region 정방향 참조: 레스토랑이 어느지역에 속하는지 확인
        # region.restaurants.all() 역참조: 이 지역에 속한 모든 레스토랑들을 조회
    )

    class Meta:
        verbose_name = "레스토랑"
        verbose_name_plural = "레스토랑"

    def __str__(self):
        return f"{self.name} {self.branch_name}" if self.branch_name else self.name
        # 지점명이 있으면 "이름 지점명", 없으면 "이름"만 반환 → 관리자 페이지에서 식별 용이.


class CuisineType(models.Model):  # 퀴진
    name = models.CharField("이름", max_length=20)

    class Meta:
        verbose_name = "음식 종류"
        verbose_name_plural = "음식 종류"

    def __str__(self):
        return self.name


class RestaurantCategory(models.Model):
    name = models.CharField("이름", max_length=20)
    cuisine_type = models.ForeignKey(
        "CuisineType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "가게 카테고리"
        verbose_name_plural = "가게 카테고리"

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_representative = models.BooleanField(
        "대표 이미지 여부", default=False
    )  # 체크하면 대표이미지로 설정됨, 기본값은 대표이미지 가 체크되지 않아서 이미지 저장후 체크여부 선택
    order = models.PositiveIntegerField("순서", null=True, blank=True)
    name = models.CharField("이름", max_length=100, null=True, blank=True)
    image = models.ImageField(
        "이미지", max_length=100, upload_to="restaurant"
    )  # 사용자가 이미지를 업로드하면 MEDIA_ROOT/restaurant/ 폴더 아래에 이미지 파일이 저장됩니다. MEDIA_ROOT가 /media/라고 가정하면
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, db_index=True
    )  # 데이터를 등록하면 생성일은 자동으로 생성됨
    updated_at = models.DateTimeField("수정일", auto_now=True, db_index=True)

    class Meta:
        verbose_name = "가게 이미지"
        verbose_name_plural = "가게 이미지"

    def __str__(self):
        return f"{self.id}:{self.image}"

    def clean(self):
        images = self.restaurant.restaurantimage_set.filter(is_representative=True)
        # 이 이미지(RestaurantImage)가 연결된 Restaurant 객체
        # .restaurantimage_set 해당 Restaurant에 연결된 모든 이미지들 (역참조)
        # .filter(is_representative=True) 그중에서 is_representative=True인 이미지들만 필터링

        if (
            self.is_representative and images.exclude(id=self.id).count() > 0
        ):  # 대표 이미지를 2개 이상 지정하지 못하도록 막는 코드
            raise ValidationError("대표 이미지는 1개만 지정 가능합니다.")
            # self는 현재 저장하려는 RestaurantImage 인스턴스입니다.
            # self.restaurant: 이 이미지가 속한 레스토랑
            # restaurantimage_set: 그 레스토랑에 속한 모든 이미지들 (RestaurantImage 객체들)
            # .filter(is_representative=True): 그중에서 대표 이미지(True) 로 설정된 것들만 가져옴
            # "이 레스토랑에 이미 대표 이미지로 설정된 다른 이미지가 있는지 확인"하는 코드입니다.


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField("이름", max_length=100)
    price = models.PositiveIntegerField("가격", default=0)
    image = models.ImageField(
        "이미지", upload_to="restaurant-menu", null=True, blank=True
    )
    # 사용자가 이미지를 업로드하면 MEDIA_ROOT/restaurant-menu/ 폴더 아래에 이미지 파일이 저장됩니다. MEDIA_ROOT가 /media/라고 가정하면

    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, db_index=True
    )  # 시간정렬을 할수도 있으니 적용하는것이 좋음
    updated_at = models.DateTimeField("수정일", auto_now=True, db_index=True)

    class Meta:
        verbose_name = "가게 메뉴"
        verbose_name_plural = "가게 메뉴"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField("제목", max_length=100)
    author = models.CharField("작성자", max_length=100)
    profile_image = models.ImageField(
        "프로필 이미지", upload_to="review-profile", blank=True, null=True
    )
    content = models.TextField("내용")
    rating = models.PositiveSmallIntegerField(  # 평점
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # 양의 정수만 허용되는 필드로 값의 범위는 0부터 32,767까지 가능하지만 아래 validators로 실제 허용 범위는 1~5로 제한됩니다.

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    social_channel = models.ForeignKey(
        "SocialChannel", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField("생성일", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("수정일", auto_now=True, db_index=True)

    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author}:{self.title}"

    # ----------사용안함-----------------
    @property
    def restaurant_name(self):
        return self.restaurant.name

    @property
    def content_partial(self):
        return self.content[:20]


# ----------사용안함-----------------


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(max_length=100, upload_to="review")
    created_at = models.DateTimeField("생성일", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("수정일", auto_now=True, db_index=True)

    class Meta:
        verbose_name = "리뷰이미지"
        verbose_name_plural = "리뷰이미지"

    def __str__(self):
        return f"{self.id}:{self.image}"


class SocialChannel(models.Model):
    name = models.CharField("이름", max_length=100)

    class Meta:
        verbose_name = "소셜채널"
        verbose_name_plural = "소셜채널"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "이름", max_length=100, unique=True
    )  # 이 필드는 중복을 허용하지 않음

    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그"

    def __str__(self):
        return self.name


class Region(models.Model):
    sido = models.CharField("광역시도", max_length=20)
    sigungu = models.CharField("시군구", max_length=20)
    eupmyeondong = models.CharField("읍면동", max_length=20)

    class Meta:
        verbose_name = "지역"
        verbose_name_plural = "지역"
        unique_together = ("sido", "sigungu", "eupmyeondong")

    def __str__(self):
        return f"{self.sido} {self.sigungu} {self.eupmyeondong}"
