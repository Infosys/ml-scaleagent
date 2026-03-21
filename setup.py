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

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlscaler",
    version="1.0.0",
    author="Infosys Limited",
    author_email="opensource@infosys.com",
    description="ML deployment management system for Kubernetes-based machine learning model scaling and orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/infosys/mlscaler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.115",
        "uvicorn[standard]>=0.24",
        "SQLAlchemy>=2.0",
        "psycopg2-binary>=2.9",
        "pydantic>=2.5",
        "pydantic-settings>=2.0",
        "typer>=0.12",
        "rich>=13.7",
        "python-dotenv>=1.0",
        "PyYAML>=6.0",
        "requests>=2.32.5",
        "kubernetes==35.0.0",
        "prettytable==3.17.0",
    ],
    entry_points={
        "console_scripts": [
            "mlscaler=app.cli.app:app",
        ],
    },
    keywords=[
        "mlops",
        "kubernetes",
        "machine-learning",
        "deployment",
        "scaling",
        "azure",
        "databricks",
        "model-serving",
    ],
    license="MIT",
)
