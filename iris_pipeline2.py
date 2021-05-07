import dagstermill as dm
from dagster import InputDefinition, ModeDefinition, fs_io_manager, pipeline, local_file_manager, Field
from dagster.utils import script_relative_path
from modules.solids import download_file

k_means_iris = dm.define_dagstermill_solid(
    "k_means_iris",
    script_relative_path("iris-kmeans_2.ipynb"),
    input_defs=[InputDefinition("path", str, description="Local path to the Iris dataset")],
    required_resource_keys={'file_manager'},
    config_schema=Field(
        int, default_value=3, is_required=False, description="The number of clusters to find"
    ),
)


@pipeline(mode_defs=[ModeDefinition(resource_defs={"io_manager": fs_io_manager, 'file_manager': local_file_manager})])
def iris_pipeline():
    k_means_iris(download_file())