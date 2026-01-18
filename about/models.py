from django.db import models

class AboutSection(models.Model):
    """
    Main accordion sections in the About page
    Each section has a title (English/Urdu) and main content
    """
    title_en = models.CharField(max_length=255, help_text="Section title in English")
    title_ur = models.CharField(max_length=255, help_text="Section title in Urdu")
    content_en = models.TextField(blank=True, help_text="Main content in English (optional if using subsections)")
    content_ur = models.TextField(blank=True, help_text="Main content in Urdu (optional if using subsections)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    default_open = models.BooleanField(default=False, help_text="Should this section be open by default?")
    is_active = models.BooleanField(default=True, help_text="Show this section on the page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self):
        return f"{self.title_en} (Order: {self.order})"


class AboutSubSection(models.Model):
    """
    Sub-sections within an AboutSection
    Used for nested content like "Daily Zikr", "Weekly Zikr", etc.
    """
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name='subsections')
    title_en = models.CharField(max_length=255, help_text="Sub-section title in English")
    title_ur = models.CharField(max_length=255, help_text="Sub-section title in Urdu")
    content_en = models.TextField(help_text="Sub-section content in English")
    content_ur = models.TextField(help_text="Sub-section content in Urdu")
    order = models.IntegerField(default=0, help_text="Display order within the parent section")
    is_active = models.BooleanField(default=True, help_text="Show this sub-section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "About Sub-Section"
        verbose_name_plural = "About Sub-Sections"

    def __str__(self):
        return f"{self.section.title_en} > {self.title_en}"


class CurrentNasheen(models.Model):
    """
    Current Masnad-e-Nasheen information
    Only one active record should exist
    """
    name_en = models.CharField(max_length=255, help_text="Full name in English")
    name_ur = models.CharField(max_length=255, help_text="Full name in Urdu")
    description_en = models.TextField(help_text="Description/biography in English")
    description_ur = models.TextField(help_text="Description/biography in Urdu")
    image = models.ImageField(upload_to='nasheen/', blank=True, null=True, help_text="Profile image")
    is_active = models.BooleanField(default=True, help_text="Is this the current active Nasheen?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Current Nasheen"
        verbose_name_plural = "Current Nasheen"
        ordering = ['-is_active', '-created_at']

    def __str__(self):
        return f"{self.name_en} (Active: {self.is_active})"


class PreviousNasheen(models.Model):
    """
    Previous Masnad-e-Nasheen for the lineage tree
    Ordered by succession order
    """
    name_en = models.CharField(max_length=255, help_text="Name in English")
    name_ur = models.CharField(max_length=255, help_text="Name in Urdu")
    order = models.IntegerField(help_text="Succession order (1 = first, 2 = second, etc.)")
    is_present = models.BooleanField(default=False, help_text="Is this the current/present Nasheen?")
    is_active = models.BooleanField(default=True, help_text="Show in lineage tree")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Previous Nasheen"
        verbose_name_plural = "Previous Nasheens"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.order}. {self.name_en}"

