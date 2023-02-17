





tmp_folder = f'/tmp/amundsen/lineage'

dict_config = {
    f'loader.filesystem_csv_atlas.{FsAtlasCSVLoader.ENTITY_DIR_PATH}': f'{tmp_folder}/entities',
    f'loader.filesystem_csv_atlas.{FsAtlasCSVLoader.RELATIONSHIP_DIR_PATH}': f'{tmp_folder}/relationships',
    f'loader.filesystem_csv_atlas.{FsAtlasCSVLoader.SHOULD_DELETE_CREATED_DIR}': False,
    f'publisher.atlas_csv_publisher.{AtlasCSVPublisher.ATLAS_CLIENT}': AtlasClient('http://localhost:21000', ('admin', 'admin')),
    f'publisher.atlas_csv_publisher.{AtlasCSVPublisher.ENTITY_DIR_PATH}': f'{tmp_folder}/entities',
    f'publisher.atlas_csv_publisher.{AtlasCSVPublisher.RELATIONSHIP_DIR_PATH}': f'{tmp_folder}/relationships',
    f'publisher.atlas_csv_publisher.{AtlasCSVPublisher.ATLAS_ENTITY_CREATE_BATCH_SIZE}': 10,
    f'extractor.openlineage_tablelineage.{OpenLineageTableLineageExtractor.CLUSTER_NAME}': 'datalab',
    f'extractor.openlineage_tablelineage.{OpenLineageTableLineageExtractor.OL_DATASET_NAMESPACE_OVERRIDE}': 'hive_table',
    f'extractor.openlineage_tablelineage.{OpenLineageTableLineageExtractor.TABLE_LINEAGE_FILE_LOCATION}': 'input_dir/openlineage_nd.json',
}


job_config = ConfigFactory.from_dict(dict_config)

task = DefaultTask(extractor=OpenLineageTableLineageExtractor(), loader=FsAtlasCSVLoader())

job = DefaultJob(conf=job_config,
                 task=task,
                 publisher=AtlasCSVPublisher())

job.launch()