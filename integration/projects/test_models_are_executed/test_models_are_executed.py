from integration.conftest import DryRunResult
from integration.utils import (
    assert_report_success,
    get_report_node_by_id,
    assert_report_node_has_columns,
)


def test_success(dry_run_result: DryRunResult):
    assert_report_success(dry_run_result)


def test_ran_correct_number_of_nodes(dry_run_result: DryRunResult):
    report = assert_report_success(dry_run_result)
    assert report.node_count == 4


def test_table_of_nodes_is_returned(dry_run_result: DryRunResult):
    report = assert_report_success(dry_run_result)
    seed_node = get_report_node_by_id(report, "seed.test_models_are_executed.my_seed")
    assert_report_node_has_columns(seed_node, {"a", "seed_b"})

    first_layer = get_report_node_by_id(
        report, "model.test_models_are_executed.first_layer"
    )
    assert_report_node_has_columns(first_layer, {"a", "b", "c"})

    second_layer = get_report_node_by_id(
        report, "model.test_models_are_executed.second_layer"
    )
    assert_report_node_has_columns(second_layer, {"a", "b", "c", "seed_b"})


def test_disabled_model_not_run(dry_run_result: DryRunResult):
    report = assert_report_success(dry_run_result)
    assert "model.test_models_are_executed.disabled_model" not in set(
        n.unique_id for n in report.nodes
    ), "Found disabled model in dry run output"


def test_model_with_all_column_types_succeeds(dry_run_result: DryRunResult):
    node = get_report_node_by_id(
        dry_run_result.report,
        "model.test_models_are_executed.model_with_all_column_types",
    )
    expected_column_names = {
        "my_string",
        "my_bytes",
        "my_integer",
        "my_int64",
        "my_float",
        "my_float64",
        "my_boolean",
        "my_bool",
        "my_timestamp",
        "my_date",
        "my_time",
        "my_datetime",
        "my_interval",
        "my_geography",
        "my_numeric",
        "my_bignumeric",
        "my_json",
        "my_struct",
        "my_struct.field_1",
        "my_struct.field_2",
        "my_struct.field_3",
        "my_struct.field_3.field_3_sub_field_1",
        "my_struct.field_3.field_3_sub_field_2",
        "my_array_of_records",
        "my_array_of_records.col_1",
        "my_array_of_records.col_2",
    }
    assert_report_node_has_columns(node, expected_column_names)
