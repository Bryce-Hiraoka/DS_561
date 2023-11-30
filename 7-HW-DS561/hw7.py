import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import re

FILE_PATTERN = 'gs://hw2-vm-bucket/webdir/*.html'

OUTPUT_FILE = 'gs://hw2-vm-bucket/main1.txt'

class ExtractLinks(beam.DoFn):
    def process(self, content):
        link_pattern = re.compile(r'<a\s+HREF="([^"]+)"', re.IGNORECASE)
        href_values = link_pattern.findall(content)
        for value in href_values:
            yield (value, 1)


def main():
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        links_per_file = (
            p
            | 'Read Files' >> beam.io.ReadFromText(FILE_PATTERN)
            | 'Extract Links' >> beam.ParDo(ExtractLinks())
            | 'Group by File' >> beam.GroupByKey()
            | 'Print Top 5 Files' >> beam.Map(print)
        )


if __name__ == "__main__":
    main()