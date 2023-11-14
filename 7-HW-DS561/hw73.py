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
            yield value

def main():
    options = PipelineOptions()

    with beam.Pipeline(options=options) as p:
        files = p | 'Take in the file' >> beam.io.ReadFromText(FILE_PATTERN)
        outgoing_links = (
            files
            | 'HrefValues' >> beam.ParDo(ExtractLinks())
            | 'CountOutgoingLinks' >> beam.combiners.Count.PerElement()
        )

        top_outgoing_links = outgoing_links | beam.transforms.combiners.Top.Of(5, key=lambda x: x[1])

        top_outgoing_links | 'Write Output' >> beam.Map(print)

if __name__ == "__main__":
    main()