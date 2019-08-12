from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.

class NameBase(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        abstract = True 
    
    def __str__(self):
        return self.name

class Ability(NameBase):
    pass

class Race_Size(NameBase):
    value = models.IntegerField(default=0)

class Language(NameBase):
    pass

#TODO: ADD RESISTANCE FEATURE_TYPE TO DB
class Feature_Type(NameBase):
    pass

#TODO: ADD LEVEL REQUIREMENT TO FEATURE (?)
class Feature(NameBase):
    description = models.TextField()
    feature_type = models.ForeignKey(Feature_Type, on_delete=models.CASCADE)
    is_choose = models.BooleanField(default=False)
    max_choose = models.IntegerField(default=0)

    class Meta:
        ordering = ['feature_type', 'name']

class Selectable_Features(models.Model):
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "%s | %s" % (self.feature, self.content_object)

class Race(NameBase):
    age = models.IntegerField(default=1)
    size = models.ForeignKey(Race_Size, on_delete=models.CASCADE)
    speed = models.IntegerField(default=5)
    languages = models.ManyToManyField(Language)
    features = models.ManyToManyField(Feature, blank=True)

class Subrace(NameBase):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature, blank=True)

class Skill(NameBase):
    description = models.TextField()
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)

class Background(NameBase):
    skills = models.ManyToManyField(Skill)
    money = models.IntegerField(default=0)
    description = models.TextField()
    tools_prof = models.ManyToManyField('Tool', blank=True)
    equipment = models.ManyToManyField('ItemQty', blank=True)
    features = models.ManyToManyField(Feature, blank=True)

class Armor_Type(NameBase):
    max_dex = models.IntegerField(default=1)
    don_time = models.CharField(max_length=255)
    doff_time = models.CharField(max_length=255)

class Armor(NameBase):
    cost = models.IntegerField(default=5)
    ac = models.IntegerField(default=1)
    armor_type = models.ForeignKey(Armor_Type, on_delete=models.CASCADE)
    min_str = models.IntegerField(default=1)
    disadv_stealth = models.BooleanField(default=False)
    weight = models.FloatField(default=1)

class Weapon_Property(NameBase):
    description = models.TextField()

class Damage_Type(NameBase):
    description = models.CharField(max_length=255)

class Weapon(NameBase):
    cost = models.IntegerField(default=1)
    damage = models.CharField(max_length=16)
    dmg_type = models.ForeignKey(Damage_Type, on_delete=models.CASCADE)
    weight = models.FloatField(default=1)
    properties = models.ManyToManyField(Weapon_Property)
    normal_range = models.IntegerField(default=5)
    max_range = models.IntegerField(default=5)

class Item_Type(NameBase): pass

class Item(NameBase):
    cost = models.IntegerField(default=1)
    weight = models.FloatField(default=1)
    description = models.TextField()
    item_type = models.ForeignKey(Item_Type, on_delete=models.CASCADE)

    class Meta:
        ordering = ['item_type', 'name']

class Tool_Type(NameBase):
    description = models.TextField()

class Tool(NameBase):
    cost = models.IntegerField(default=1)
    weight = models.FloatField(default=1)
    tool_type = models.ForeignKey(Tool_Type, on_delete=models.CASCADE)

class Magic_School(NameBase):
    pass

class Spell(NameBase):
    level = models.IntegerField(default=0)  
    spell_range = models.IntegerField(default=0)
    casting_time = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    is_vocal = models.BooleanField(default=True)
    is_somatic = models.BooleanField(default=True)
    is_material = models.BooleanField(default=True)
    components = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField()
    school = models.ForeignKey(Magic_School, on_delete=models.CASCADE)
    can_ritual = models.BooleanField(default=False)
    is_concentration = models.BooleanField(default=False)

class Alignment(NameBase):
    pass

class Spell_Slot(models.Model):
    level = models.IntegerField(default=1)
    qty = models.IntegerField(default=1)

    def __str__(self):
        if self.level == 1:
            return "1st (%s)" % self.qty
        elif self.level == 2:
            return "2nd (%s)" % self.qty
        elif self.level == 3:
            return "3rd (%s)" % self.qty
        return "%sth (%s)" % (self.level, self.qty)

class Class_Base(NameBase):
    hitdie = models.IntegerField(default=1)
    saving_throws = models.ManyToManyField(Ability)
    available_skills = models.ManyToManyField(Skill)
    weap_prof = models.ManyToManyField(Weapon, blank=True)
    armor_prof = models.ManyToManyField(Armor, blank=True)
    tool_prof = models.ManyToManyField(Tool, blank=True)
    max_skills = models.IntegerField(default=1)
    spells = models.ManyToManyField(Spell, blank=True)

class Class_Level(models.Model):
    level = models.IntegerField(default=1)
    prof_bonus = models.IntegerField(default=1)
    features = models.ManyToManyField(Feature, blank=True) 
    class_base = models.ForeignKey(Class_Base, on_delete=models.CASCADE)
    spell_slots = models.ManyToManyField(Spell_Slot, blank=True)
    cantrips = models.IntegerField(default=0)
    spells_known = models.IntegerField(default=0)

    def __str__(self):
        return "%s (%s)" % (self.class_base, self.level)

    def get_equipment_options(self):
        return self.features.filter(feature_type__name='Equipment')

    def get_features(self):
        return self.features.exclude(feature_type__name='Equipment')

class Subclass_Base(NameBase):
    class_base = models.ForeignKey(Class_Base, on_delete=models.CASCADE)
    level_chosen = models.IntegerField(default=1)

class Subclass_Level(models.Model):
    level = models.IntegerField(default=1)
    features = models.ManyToManyField(Feature, blank=True)
    subclass_base = models.ForeignKey(Subclass_Base, on_delete=models.CASCADE)
    spell_slots = models.ManyToManyField(Spell_Slot, blank=True)
    cantrips = models.IntegerField(default=0)
    spells_known = models.IntegerField(default=0)

    def __str__(self):
        return "%s (%s)" % (self.subclass_base, self.level)


class Character(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField(default=1)
    class_base = models.ForeignKey(Class_Base, on_delete=models.CASCADE)
    class_levels = models.ManyToManyField(Class_Level)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    subrace = models.ForeignKey(Subrace, on_delete=models.CASCADE, blank=True, null=True)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE)
    hp = models.IntegerField(default=0)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)
    saving_throws = models.ManyToManyField(Ability)
    skills_prof = models.ManyToManyField(Skill)
    weap_prof = models.ManyToManyField(Weapon)
    armor_prof = models.ManyToManyField(Armor)
    tool_prof = models.ManyToManyField(Tool)
    languages = models.ManyToManyField(Language)
    features = models.ManyToManyField(Feature)
    known_spells = models.ManyToManyField(Spell, related_name='known_by')
    prepared_spells = models.ManyToManyField(Spell, related_name='prepared_by')
    def __str__(self):
        return "%s - %s(%i)" % (self.name, self.class_base, self.level)

class Inventory(models.Model):
    weapons = models.ManyToManyField(Weapon)
    armors = models.ManyToManyField(Armor)
    tools = models.ManyToManyField(Tool)
    money = models.IntegerField(default=0)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

class ItemQty(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, blank=True, null=True)
    armor = models.ForeignKey(Armor, on_delete=models.CASCADE, blank=True, null=True)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, blank=True, null=True)
    pack = models.ForeignKey('Equipment_Pack', on_delete=models.CASCADE, blank=True, null=True)

    qty = models.FloatField(default=0)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        if self.item:
            return "%s (%i)" % (self.item, self.qty)
        elif self.tool:
            return "%s (%i)" % (self.tool, self.qty)
        elif self.armor:
            return "%s (%i)" % (self.armor, self.qty)
        elif self.pack:
            return "%s (%i)" % (self.pack, self.qty)
        else:
            return "%s (%i)" % (self.weapon, self.qty)

class ItemBundle(models.Model):
    items = models.ManyToManyField(ItemQty)
    bundle = models.ManyToManyField('ItemBundle', blank=True)
    is_choose = models.BooleanField(default=False)
    max_choose = models.IntegerField(default=1)

    def __str__(self):
        weapons = []
        tools = []
        items = []
        name = ""
        for i in self.items.all():
            name += str(i) + " - " 
            if i.weapon:
                weapons.append(i.weapon)
            if i.tool:
                tools.append(i.tool)
            if i.item:
                items.append(i.item)
        for b in self.bundle.all():
            name += str(b) + " - "
        weapons = set(weapons)
        tools = set(tools)
        items = set(items)

        if set(Weapon.objects.filter(properties__name='Simple')) == weapons:
            return "Simple Weapons - Choose %s" % self.max_choose
        elif set(Weapon.objects.filter(properties__name='Simple').filter(properties__name='Melee')) == weapons:
            return "Simple Melee Weapons - Choose %s" % self.max_choose
        elif set(Weapon.objects.filter(properties__name='Simple').filter(properties__name='Ranged')) == weapons:
            return "Simple Ranged Weapons - Choose %s" % self.max_choose
        elif set(Weapon.objects.filter(properties__name='Martial')) == weapons:
            return "Martial Weapons - Choose %s" % self.max_choose
        elif set(Weapon.objects.filter(properties__name='Martial').filter(properties__name='Melee')) == weapons:
            return "Martial Melee Weapons - Choose %s" % self.max_choose
        elif set(Weapon.objects.filter(properties__name='Martial').filter(properties__name='Ranged')) == weapons:
            return "Martial Ranged Weapons - Choose %s" % self.max_choose
        elif set(Tool.objects.filter(tool_type__name='Musical Instrument')) == tools:
            return "Musical Intruments - Choose %s" % self.max_choose
        elif set(Item.objects.filter(item_type__name='Holy Symbol')) == items:
            return "Holy Symbol - Choose %s" % self.max_choose
        return name


class Equipment_Pack(NameBase):
    cost = models.IntegerField(default=1)
    items = models.ManyToManyField(ItemQty)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, blank=True, null=True)