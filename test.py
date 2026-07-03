from app.controllers.data_record import StaticData;

static = StaticData("castle_layout.json");
color = static.clone_data("harry");
print(color);

