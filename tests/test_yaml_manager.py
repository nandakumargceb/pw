from pathlib import Path

from src.common.reusable_functions import (
    Read_Yaml_Test_Data,
    Write_Yaml_Test_Data,
    extract_yaml_data,
    update_yaml_data,
)


def test_travel_mug_30oz_agave_teal_bride_design():
    file_path = Path("Test_Data") / "SIT.yaml"

    read_value = Read_Yaml_Test_Data("Field_1")
    assert read_value == "Agave Teal"

    rows = extract_yaml_data(file_path=file_path)
    assert len(rows) >= 1
    assert rows[0]["Test_Case_Name"] == "test_travel_mug_30oz_agave_teal_bride_design"
    assert str(rows[0]["Execute"]).strip().upper() == "YES"

    update_yaml_data(
        "test_travel_mug_30oz_agave_teal_bride_design",
        "Comments",
        "Updated via YAML test",
        file_path=file_path,
    )

    updated = extract_yaml_data(file_path=file_path)
    assert updated[0]["Comments"] == "Updated via YAML test"

    Write_Yaml_Test_Data("Comments", "Test completed successfully")
    assert Read_Yaml_Test_Data("Comments") == "Test completed successfully"
