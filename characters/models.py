from django.db import models

# Create your models here.
class Team(models.Model):
    name = models.TextField("Название команды")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self) -> str:
        return self.name

class Position(models.Model):
    name = models.TextField("Позиция на поле")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"

    def __str__(self) -> str:
        return self.name

class Skills(models.Model):
    name = models.TextField("Способность")
    description = models.TextField("Описание способности", null=True)
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Способность"
        verbose_name_plural = "Способности"

    def __str__(self) -> str:
        return self.name
    
class ContentType(models.Model):
    name = models.TextField("Тип медиа")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Тип контента"
        verbose_name_plural = "Типы контента"

    def __str__(self) -> str:
        return self.name

class Character(models.Model):
    name = models.TextField("Имя")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="characters")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Персонаж"
        verbose_name_plural = "Персонажи"

class Content(models.Model):
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    episode_name = models.TextField("Название эпизода") #Серия\Глава
    episode = models.IntegerField("Номер эпизода")      #Серия\Глава
    volume = models.IntegerField("Номер раздела")       #Том\Сезон
    description = models.TextField("Описание эпизода")
    picture = models.ImageField("Изображение", null=True, upload_to="characters")
    user = models.ForeignKey("auth.User", verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

class User(models.Model):
  name = models.TextField("Имя")

  class Meta:
    verbose_name = "Пользователь"
    verbose_name_plural = "Пользователи"

  def str(self) -> str:
    return self.name