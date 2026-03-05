class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        # Таблица сотрудников
        self.employees = {
            1: ["SN001", "Петров", "Инспектор", 1],
            2: ["SN002", "Сидоров", "Руководитель", 2]
        }
        # Таблица объектов
        self.railway_objects = {
            1: ["station", "Станция Новосибирск", "км 10", 1],
            2: ["crossing", "Переезд №45", "км 25", 1],
            3: ["section", "Перегон А-Б", "км 30-40", 1]
        }
        # Таблица инцидентов
        self.incidents = {
            1: ["15.02.2025", 2, "Нарушение", "Проезд на запрещающий сигнал", "Открыт", 1]
        }
        self.incidents_count = 1

    def add_incident(self, date, object_id, incident_type, description, reporter_id):
        new_incident_id = self.incidents_count + 1
        self.incidents[new_incident_id] = [date, object_id, incident_type, description, "Открыт", reporter_id]
        self.incidents_count += 1

    def update_incident(self, id, new_date, new_type, new_description, new_status):
        if id in self.incidents:
            self.incidents[id][0] = new_date
            self.incidents[id][2] = new_type
            self.incidents[id][3] = new_description
            self.incidents[id][4] = new_status

    def view_incident(self, id):
        if id in self.incidents:
            return self.incidents[id]
        else:
            return "Инцидент не найден"

    def get_all_incidents(self):
        return self.incidents


class SafetyManagement:
    def __init__(self, db_name):
        self.db = DataBase(db_name)

    def login(self, service_number, name):
        for emp_id, (emp_sn, emp_name, position, access_level) in self.db.employees.items():
            if emp_sn == service_number and emp_name == name:
                return emp_id, position, access_level
        return None, None, None

    def view_all_incidents(self, user_id, access_level):
        if user_id in self.db.employees:
            all_incidents = self.db.get_all_incidents()
            if access_level == 1:  # Инспектор видит только свои
                return {k: v for k, v in all_incidents.items() if v[5] == user_id}
            return all_incidents  # Руководитель видит все
        else:
            return "Пользователь не найден"

    def add_incident(self, date, object_id, incident_type, description, reporter_id):
        self.db.add_incident(date, object_id, incident_type, description, reporter_id)

    def update_incident(self, id, new_date, new_type, new_description, new_status):
        self.db.update_incident(id, new_date, new_type, new_description, new_status)

    def view_incident(self, id):
        return self.db.view_incident(id)

    def get_object_name(self, object_id):
        if object_id in self.db.railway_objects:
            return self.db.railway_objects[object_id][1]
        return "Неизвестный объект"


class InteractionMenu():
    def __init__(self, db_name):
        self.management_system = SafetyManagement(db_name)
        self.logged_in = False
        self.current_user_id = None
        self.current_position = None
        self.current_access_level = None

    def start_menu(self):
        while True:
            print("\n===== СИСТЕМА БЕЗОПАСНОСТИ ЖД ТРАНСПОРТА =====")
            print("1. Войти в систему")
            print("2. Просмотреть все инциденты")
            print("3. Добавить инцидент")
            print("4. Обновить инцидент")
            print("5. Просмотреть инцидент по ID")
            print("6. Выйти")
            action = input("Введите ваш выбор: ")

            if action == "1":
                self.login_menu()
            elif action == "2":
                self.view_all_incidents_menu()
            elif action == "3":
                self.add_incident_menu()
            elif action == "4":
                self.update_incident_menu()
            elif action == "5":
                self.view_incident_menu()
            elif action == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор, попробуйте снова.")

    def login_menu(self):
        if self.logged_in:
            print("Вы уже вошли в систему!")
            return
        service_number = input("Введите ваш служебный номер (например, SN001): ")
        name = input("Введите ваше имя (например, Петров): ")
        user_id, position, access_level = self.management_system.login(service_number, name)
        if user_id:
            self.logged_in = True
            self.current_user_id = user_id
            self.current_position = position
            self.current_access_level = access_level
            print(f"Добро пожаловать, {name}! Должность: {position}")
        else:
            print("Неверные учетные данные, попробуйте снова.")

    def view_all_incidents_menu(self):
        if not self.logged_in:
            print("Сначала войдите в систему!")
            return
        incidents = self.management_system.view_all_incidents(self.current_user_id, self.current_access_level)
        if incidents == "Пользователь не найден":
            print("Пользователь не найден.")
        else:
            print("\n===== СПИСОК ИНЦИДЕНТОВ =====")
            for incident_id, incident_data in incidents.items():
                object_name = self.management_system.get_object_name(incident_data[1])
                print(f"ID: {incident_id} | Дата: {incident_data[0]} | Объект: {object_name}")
                print(f"Тип: {incident_data[2]} | Статус: {incident_data[4]}")
                print("-" * 60)

    def add_incident_menu(self):
        if not self.logged_in:
            print("Сначала войдите в систему!")
            return
        date = input("Введите дату (ДД.ММ.ГГГГ): ")
        print("Доступные объекты:")
        for obj_id, obj_data in self.management_system.db.railway_objects.items():
            print(f"  {obj_id}: {obj_data[1]} ({obj_data[0]})")
        object_id = int(input("Введите ID объекта: "))
        incident_type = input("Введите тип инцидента (Нарушение/Авария/Инцидент): ")
        description = input("Введите описание: ")
        self.management_system.add_incident(date, object_id, incident_type, description, self.current_user_id)
        print("Инцидент успешно добавлен!")

    def update_incident_menu(self):
        if not self.logged_in:
            print("Сначала войдите в систему!")
            return
        incident_id = int(input("Введите ID инцидента для обновления: "))
        new_date = input("Введите новую дату (ДД.ММ.ГГГГ): ")
        new_type = input("Введите новый тип: ")
        new_description = input("Введите новое описание: ")
        new_status = input("Введите новый статус (Открыт/В работе/Закрыт): ")
        self.management_system.update_incident(incident_id, new_date, new_type, new_description, new_status)
        print(f"Инцидент {incident_id} успешно обновлён!")

    def view_incident_menu(self):
        if not self.logged_in:
            print("Сначала войдите в систему!")
            return
        incident_id = int(input("Введите ID инцидента для просмотра: "))
        incident = self.management_system.view_incident(incident_id)
        if incident == "Инцидент не найден":
            print(f"Инцидент {incident_id} не найден.")
        else:
            object_name = self.management_system.get_object_name(incident[1])
            print(f"\n===== ИНЦИДЕНТ ID: {incident_id} =====")
            print(f"Дата: {incident[0]}")
            print(f"Объект: {object_name}")
            print(f"Тип: {incident[2]}")
            print(f"Описание: {incident[3]}")
            print(f"Статус: {incident[4]}")
            print(f"ID ответственного: {incident[5]}")


if __name__ == "__main__":
    db_name = "железнодорожная_безопасность"
    interaction_menu = InteractionMenu(db_name)
    interaction_menu.start_menu()
