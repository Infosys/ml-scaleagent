# /******************************************************************
# © 2025-2026 Infosys Limited, Bangalore, India. All Rights Reserved.
# Infosys believes the information in this document is accurate as of its publication date;
# such information is subject to change without notice. Infosys acknowledges the proprietary
# rights of other companies to the trademarks, product names and such other intellectual property
# rights mentioned in this document. Except as expressly permitted, neither this documentation nor
# any part of it may be reproduced, stored in a retrieval system, or transmitted in any form or by
# any means, electronic, mechanical, printing, photocopying, recording or otherwise, without the prior
# permission of Infosys Limited and/or any named intellectual property rights holders under this document.
# *******************************************************************/

# PROPRIETARY NOTICE
# This software is confidential and proprietary information of Infosys Limited.
# You shall not disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into with Infosys Limited.

import sys
import yaml
import psycopg2
import subprocess
import importlib.util
import logging

logger = logging.getLogger(__name__)

# Ensure psycopg2-binary is installed


def ensure_psycopg2():
    try:
        if importlib.util.find_spec("psycopg2") is None:
            logger.info("[startup] Installing psycopg2-binary...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install",
                     "psycopg2-binary"])
                logger.info(
                    "[startup] psycopg2-binary installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"[startup] Failed to install psycopg2-binary: {e}")
                raise
    except Exception as e:
        logger.error(f"[startup] Error checking/installing psycopg2: {e}")
        raise


try:
    ensure_psycopg2()
except Exception as e:
    logger.error(f"[startup] Failed to ensure psycopg2 availability: {e}")
    sys.exit(1)


def check_postgres_health():
    try:
        try:
            with open("./app/config.yaml", "r") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Config file is empty")
        except FileNotFoundError:
            logger.error("[startup] Config file not found at ./app/config.yaml")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"[startup] Invalid YAML in config file: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"[startup] Error reading config file: {e}")
            sys.exit(1)

        try:
            db_url = config["db_config"]["database_url"]
            if not db_url:
                raise ValueError("Database URL is empty")
        except KeyError as e:
            logger.error(f"[startup] Missing database configuration key: {e}")
            sys.exit(1)

        # Parse DB URL for psycopg2
        import re
        try:
            m = re.match(r"postgresql\+psycopg2://(.*?):(.*?)@(.*?):(\d+)/(.*)", db_url)
            if not m:
                logger.error("[startup] Invalid database_url format in config.yaml")
                sys.exit(1)
            user, password, host, port, dbname = m.groups()
        except Exception as e:
            logger.error(f"[startup] Error parsing database URL: {e}")
            sys.exit(1)

        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port,
                connect_timeout=5
            )
        except psycopg2.OperationalError as e:
            logger.error(f"[startup] Failed to connect to PostgreSQL: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"[startup] Unexpected error connecting to database: {e}")
            sys.exit(1)

        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            cur.close()
            conn.close()
            logger.info("startup ok: postgres healthy")
        except psycopg2.Error as e:
            logger.error(f"[startup] Database query failed: {e}")
            if conn:
                conn.close()
            sys.exit(1)
        except Exception as e:
            logger.error(f"[startup] Unexpected error during health check: {e}")
            if conn:
                conn.close()
            sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        logger.error(f"[startup] Postgres health check failed: {e}")
        sys.exit(1)

# if __name__ == "__main__":
#     check_postgres_health()
