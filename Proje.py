import random  

class Character:  
    def __init__(self, name, Cakra, inventory=None):  
        self.name = name  
        self.Cakra = Cakra  
        self.inventory = inventory or []  
        
    def attack(self):  
        if self.inventory:  
            weapon = random.choice([item for item in self.inventory if isinstance(item, Weapon)])  
            return weapon.get_attack_power(), weapon.miss_attack()  
        return 0, False  

    def take_damage(self, damage):  
        self.Cakra -= damage  
        print(f"{self.name}, {damage} hasar aldi. Kalan cakra: {self.Cakra}")  

    def Cakra_check(self):  
        return self.Cakra > 0  

    def add_item(self, item):  
        self.inventory.append(item)  
    
    def delete_item(self, item):  
        if item in self.inventory:  
            self.inventory.remove(item)  
    
    def drink_CakraDestegi(self):  
        cakra_destegi = next((item for item in self.inventory if isinstance(item, CakraDestegi)), None)  
        if cakra_destegi:  
            self.Cakra += cakra_destegi.heal_amount  
            print(f"{self.name}, en sevdigi seyi tuketti ve {cakra_destegi.heal_amount} cakra geri kazandi.")  
            self.delete_item(cakra_destegi)  


class Item:  
    def __init__(self, name, weight):  
        self.name = name  
        self.weight = weight  

    def use(self):  
        pass  


class Weapon(Item):  
    def __init__(self, name, weight, damage):  
        super().__init__(name, weight)  
        self.damage = damage  
        self.luck_factor = random.uniform(0.8, 3)  

    def get_attack_power(self):  
        return self.damage * self.luck_factor  
    
    def miss_attack(self):  
        return random.random() < 0.2  


class DefenseItem(Item):  
    def __init__(self, name, weight, defense_value):  
        super().__init__(name, weight)  
        self.defense_value = defense_value  
        self.luck_factor = random.uniform(0.8, 1.2)  

    def get_defense_power(self):  
        return self.defense_value * self.luck_factor  


class Shield(DefenseItem):  
    def __init__(self, name, weight, defense_value, durability):  
        super().__init__(name, weight, defense_value)  
        self.durability = durability  

    def use(self):  
        if self.durability > 0:  
            self.durability -= 1  
            return True  
        return False  


class CakraDestegi(Item):  
    def __init__(self, name, weight, heal_amount):  
        super().__init__(name, weight)  
        self.heal_amount = heal_amount  


def fight(character1, character2):  
    turn = 0  
    while character1.Cakra_check() and character2.Cakra_check():  
        attacker = character1 if turn % 2 == 0 else character2  
        defender = character2 if turn % 2 == 0 else character1  

        print(f"\n{attacker.name}, {defender.name}'e saldiriyor.")  
        attack_power, missed = attacker.attack()  

        if missed:  
            print(f"{attacker.name}, saldiriya kacirdi!")  
            turn += 1  
            continue  
        
        if attack_power == 0:  
            print(f"{attacker.name}, saldiracak silahi yok.")  
            turn += 1  
            continue  

        defense_power = 0  
        for item in defender.inventory:  
            if isinstance(item, DefenseItem):  
                defense_power += item.get_defense_power()  

        damage = max(0, attack_power - defense_power)  
        defender.take_damage(damage)  
    
        if random.random() < 0.2:  # %20 sansla Cakra Destegi icme  
            defender.drink_CakraDestegi()  
        
        turn += 1  
    
    winner = character1 if character1.Cakra_check() else character2  
    print(f"\n{winner.name} kazandi!")  


char1 = Character("Dexter", 100, [  
    Weapon("Enjektor", 5, 20),   
    Shield("Naylon Kiyafet", 10, 15, 3),   
    CakraDestegi("Portakal Suyu", 1, 15)  
])  

char2 = Character("Hannibal", 80, [  
    Weapon("Asci Bicagi", 3, 25),   
    DefenseItem("Takim Elbise", 2, 10),   
    CakraDestegi("Biftek", 2, 30)  
])  

fight(char1, char2)


