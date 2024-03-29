from typing import Optional, Any

from src.agent import constants


class _ConfigProvider:
    def __init__(self):
        metrics = {
            'node': {
                'node_cpu_usage_total': '''
                        sum(
                              (1 - sum without (mode) (rate(node_cpu_seconds_total{job="node-exporter", mode=~"idle|iowait|steal", instance="10.224.0.4:9100"}[3600s])))
                            / ignoring(cpu) group_left count without (cpu, mode) (node_cpu_seconds_total{job="node-exporter", mode="idle", instance="10.224.0.4:9100"})
                        ) by (instance)
                ''',
                # todo, what exactly should be in this query? Is it total.. or total for a period?
                'node_network_total_bytes': '''
                    sum_over_time(node_network_transmit_bytes_total[3600s]) + sum_over_time(node_network_receive_bytes_total[3600s])
                ''',
            },
        }
        self.config = {
            'prometheus_url': 'http://localhost:8428',
            'log_file_path': 'logs/agent.log',
            # todo metric config loader?
            'metric_queries': self._get_metric_queries(metrics),
            'metric_groups': self._get_metric_groups(metrics),
            'offset_file_path': constants.OFFSET_FILE_PATH,
            'state_file_path': constants.STATE_FILE_PATH,
            'interval': '1h',
            'initial_offset': 1657284343,
            'metrics_dir': constants.METRICS_DIR,
            'grouped_metrics_dir': constants.GROUPED_METRICS_DIR,
        }
        self._load_config()

    def get(self, key: str, default=None) -> Optional[Any]:
        return self.config.get(key, default)

    def __getitem__(self, key):
        return self.config[key]

    def _load_config(self):
        pass

    @staticmethod
    def _get_metric_queries(metrics) -> dict:
        queries = {}
        for _, metric_queries in metrics.items():
            queries |= metric_queries
        return queries

    @staticmethod
    def _get_metric_groups(metrics) -> dict:
        return {group_name: list(metric_queries) for group_name, metric_queries in metrics.items()}


config_provider = _ConfigProvider()
