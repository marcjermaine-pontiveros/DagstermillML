# Data Science with Notebooks

- [Notebooks as solids](https://docs.dagster.io/integrations/dagstermill#notebooks-as-solids)
- [Expressing dependencies](https://docs.dagster.io/integrations/dagstermill#expressing-dependencies)
- [The notebook context](https://docs.dagster.io/integrations/dagstermill#the-notebook-context)
- [Results and custom materialziations](https://docs.dagster.io/integrations/dagstermill#results-and-custom-materializations)

Fast iteration, the literate combination of arbitrary code with markdown blocks, and inline plotting make notebooks an indispensible tool for data science. 
The Dagstermill package makes it straightforward to run notebooks using the Dagster tools and to integrate them into data pipelines with heterogeneous solids: 
for instance, Spark jobs, SQL statements run against a data warehouse, or arbitrary Python code.

```shell
pip install dagstermill
```

Dagstermill lets you:
- Run notebooks as solids in heterogeneous data pipelines with minimal changes to notebook code
- Define data dependencies to flow inputs and outputs between notebooks, and between notebooks and other solids
- Use Dagster resources, and the Dagster config system, from inside notebooks
- Aggregate notebook logs with logs from other Dagster solids
- Yield custom materializations and other Dagster events from your notebook code

Our goal is to make it unnecessary to go through a tedious "productionization" process where code developed in notebooks must be translated into some other (less readable and interpretable) format in order to be integrated into production workflows. Instead, we can use notebooks as solids directly, with minimal, incremental metadata declarations to integrate them into pipelines that may also contain arbitrary heterogeneous solids.

## Notebooks as solids

Let's consider the classic Iris dataset (1, 2), collected in 1936 by the American botanist Edgar Anderson and made famous by statistician Ronald Fisher. The Iris dataset is a basic example in machine learning because it contains three classes of observation, one of which is straightforwardly linearly separable from the other two, which in turn can only be distinguished by more sophisticated methods.

[K-means clustering for the Iris data set](https://github.com/dagster-io/dagster/blob/0.10.8/examples/docs_snippets/docs_snippets/legacy/data_science/iris-kmeans.ipynb)

Like many notebooks, this example does some fairly sophisticated work, producing diagnostic plots and a (flawed) statistical model -- which are then locked away in the .ipynb format, can only be reproduced using a complex Jupyter setup, and are only programmatically accessible within the notebook context.

We can simply turn a notebook into a solid using `define_dagstermill_solid`. Once we create a solid, we can start to make its outputs more accessible.

```python
import dagstermill as dm
from dagster import ModeDefinition, fs_io_manager, local_file_manager, pipeline
from dagster.utils import script_relative_path

k_means_iris = dm.define_dagstermill_solid(
    "k_means_iris", script_relative_path("iris-kmeans.ipynb")
)


@pipeline(
    mode_defs=[
        ModeDefinition(
            resource_defs={"io_manager": fs_io_manager, "file_manager": local_file_manager}
        )
    ]
)
def iris_pipeline():
    k_means_iris()
```

This is the simplest form of notebook integration -- we don't actually have to make any changes in the notebook itself to run it using the Dagster tooling. Just run:

```shell
dagit -f iris_pipeline.py
```