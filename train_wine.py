{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "f7fbbfc9",
   "metadata": {
    "papermill": {
     "duration": 0.020979,
     "end_time": "2023-08-20T11:07:16.427567",
     "exception": false,
     "start_time": "2023-08-20T11:07:16.406588",
     "status": "completed"
    },
    "tags": []
   },
   "source": [
    "# Wine Quality Prediction "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "87a85497",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:16.472803Z",
     "iopub.status.busy": "2023-08-20T11:07:16.472367Z",
     "iopub.status.idle": "2023-08-20T11:07:18.094864Z",
     "shell.execute_reply": "2023-08-20T11:07:18.093978Z"
    },
    "papermill": {
     "duration": 1.6473,
     "end_time": "2023-08-20T11:07:18.097635",
     "exception": false,
     "start_time": "2023-08-20T11:07:16.450335",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "import os \n",
    "from tkinter import E\n",
    "import argparse\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import sklearn\n",
    "from sklearn.linear_model import ElasticNet\n",
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.linear_model import ElasticNet\n",
    "import mlflow\n",
    "import mlflow.sklearn\n",
    "from mlflow.tracking import MlflowClient"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6c13ffa8",
   "metadata": {},
   "source": [
    "# Hyper Paramater Tunning"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "61d7e4dc",
   "metadata": {},
   "outputs": [],
   "source": [
    "from hyperopt import fmin,tpe,hp,STATUS_OK,Trials\n",
    "from hyperopt.pyll import scope"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "e94aaf3a",
   "metadata": {},
   "source": [
    "# ML flow Tracking"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "40afad44",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Active run_id: a3478ce73e284ea69540d524dd4c25e6\n"
     ]
    }
   ],
   "source": [
    "import mlflow\n",
    "#mlflow.set_tracking_uri('http://localhost:5000')\n",
    "#mlflow.set_tracking_uri(\"sqlite:///winequality2.db\")\n",
    "mlflow.set_tracking_uri(\"http://localhost:5000\")\n",
    "mlflow.set_experiment(\"wine_quality_2\")\n",
    "mlflow.start_run()\n",
    "run = mlflow.active_run()\n",
    "print(\"Active run_id: {}\".format(run.info.run_id))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "d0270da4",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.142343Z",
     "iopub.status.busy": "2023-08-20T11:07:18.141275Z",
     "iopub.status.idle": "2023-08-20T11:07:18.170771Z",
     "shell.execute_reply": "2023-08-20T11:07:18.169700Z"
    },
    "papermill": {
     "duration": 0.05445,
     "end_time": "2023-08-20T11:07:18.173475",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.119025",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine=pd.read_csv('H:\\Metaverse\\MLprob\\mlflow\\wine-quality.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "8efe4894",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.220726Z",
     "iopub.status.busy": "2023-08-20T11:07:18.219980Z",
     "iopub.status.idle": "2023-08-20T11:07:18.250163Z",
     "shell.execute_reply": "2023-08-20T11:07:18.249262Z"
    },
    "papermill": {
     "duration": 0.05703,
     "end_time": "2023-08-20T11:07:18.252445",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.195415",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>fixed acidity</th>\n",
       "      <th>volatile acidity</th>\n",
       "      <th>citric acid</th>\n",
       "      <th>residual sugar</th>\n",
       "      <th>chlorides</th>\n",
       "      <th>free sulfur dioxide</th>\n",
       "      <th>total sulfur dioxide</th>\n",
       "      <th>density</th>\n",
       "      <th>pH</th>\n",
       "      <th>sulphates</th>\n",
       "      <th>alcohol</th>\n",
       "      <th>quality</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>7.0</td>\n",
       "      <td>0.27</td>\n",
       "      <td>0.36</td>\n",
       "      <td>20.7</td>\n",
       "      <td>0.045</td>\n",
       "      <td>45.0</td>\n",
       "      <td>170.0</td>\n",
       "      <td>1.0010</td>\n",
       "      <td>3.00</td>\n",
       "      <td>0.45</td>\n",
       "      <td>8.8</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>6.3</td>\n",
       "      <td>0.30</td>\n",
       "      <td>0.34</td>\n",
       "      <td>1.6</td>\n",
       "      <td>0.049</td>\n",
       "      <td>14.0</td>\n",
       "      <td>132.0</td>\n",
       "      <td>0.9940</td>\n",
       "      <td>3.30</td>\n",
       "      <td>0.49</td>\n",
       "      <td>9.5</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>8.1</td>\n",
       "      <td>0.28</td>\n",
       "      <td>0.40</td>\n",
       "      <td>6.9</td>\n",
       "      <td>0.050</td>\n",
       "      <td>30.0</td>\n",
       "      <td>97.0</td>\n",
       "      <td>0.9951</td>\n",
       "      <td>3.26</td>\n",
       "      <td>0.44</td>\n",
       "      <td>10.1</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>7.2</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.32</td>\n",
       "      <td>8.5</td>\n",
       "      <td>0.058</td>\n",
       "      <td>47.0</td>\n",
       "      <td>186.0</td>\n",
       "      <td>0.9956</td>\n",
       "      <td>3.19</td>\n",
       "      <td>0.40</td>\n",
       "      <td>9.9</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>7.2</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.32</td>\n",
       "      <td>8.5</td>\n",
       "      <td>0.058</td>\n",
       "      <td>47.0</td>\n",
       "      <td>186.0</td>\n",
       "      <td>0.9956</td>\n",
       "      <td>3.19</td>\n",
       "      <td>0.40</td>\n",
       "      <td>9.9</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   fixed acidity  volatile acidity  citric acid  residual sugar  chlorides  \\\n",
       "0            7.0              0.27         0.36            20.7      0.045   \n",
       "1            6.3              0.30         0.34             1.6      0.049   \n",
       "2            8.1              0.28         0.40             6.9      0.050   \n",
       "3            7.2              0.23         0.32             8.5      0.058   \n",
       "4            7.2              0.23         0.32             8.5      0.058   \n",
       "\n",
       "   free sulfur dioxide  total sulfur dioxide  density    pH  sulphates  \\\n",
       "0                 45.0                 170.0   1.0010  3.00       0.45   \n",
       "1                 14.0                 132.0   0.9940  3.30       0.49   \n",
       "2                 30.0                  97.0   0.9951  3.26       0.44   \n",
       "3                 47.0                 186.0   0.9956  3.19       0.40   \n",
       "4                 47.0                 186.0   0.9956  3.19       0.40   \n",
       "\n",
       "   alcohol  quality  \n",
       "0      8.8        6  \n",
       "1      9.5        6  \n",
       "2     10.1        6  \n",
       "3      9.9        6  \n",
       "4      9.9        6  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "09df988d",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.546165Z",
     "iopub.status.busy": "2023-08-20T11:07:18.545444Z",
     "iopub.status.idle": "2023-08-20T11:07:18.551174Z",
     "shell.execute_reply": "2023-08-20T11:07:18.550231Z"
    },
    "papermill": {
     "duration": 0.031853,
     "end_time": "2023-08-20T11:07:18.553665",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.521812",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine.columns=wine.columns.str.strip()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "fd1698f5",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.600641Z",
     "iopub.status.busy": "2023-08-20T11:07:18.599921Z",
     "iopub.status.idle": "2023-08-20T11:07:18.605483Z",
     "shell.execute_reply": "2023-08-20T11:07:18.604637Z"
    },
    "papermill": {
     "duration": 0.031738,
     "end_time": "2023-08-20T11:07:18.607817",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.576079",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine.columns=wine.columns.str.lower()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "5d84beed",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.654216Z",
     "iopub.status.busy": "2023-08-20T11:07:18.653526Z",
     "iopub.status.idle": "2023-08-20T11:07:18.659066Z",
     "shell.execute_reply": "2023-08-20T11:07:18.658203Z"
    },
    "papermill": {
     "duration": 0.031185,
     "end_time": "2023-08-20T11:07:18.661339",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.630154",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine.columns=wine.columns.str.replace(' ','_')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "1c57afe2",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.707839Z",
     "iopub.status.busy": "2023-08-20T11:07:18.707190Z",
     "iopub.status.idle": "2023-08-20T11:07:18.714274Z",
     "shell.execute_reply": "2023-08-20T11:07:18.713226Z"
    },
    "papermill": {
     "duration": 0.033301,
     "end_time": "2023-08-20T11:07:18.716517",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.683216",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',\n",
       "       'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',\n",
       "       'ph', 'sulphates', 'alcohol', 'quality'],\n",
       "      dtype='object')"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "fa9b4ed0",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.762636Z",
     "iopub.status.busy": "2023-08-20T11:07:18.762000Z",
     "iopub.status.idle": "2023-08-20T11:07:18.802363Z",
     "shell.execute_reply": "2023-08-20T11:07:18.801469Z"
    },
    "papermill": {
     "duration": 0.066524,
     "end_time": "2023-08-20T11:07:18.804918",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.738394",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>fixed_acidity</th>\n",
       "      <th>volatile_acidity</th>\n",
       "      <th>citric_acid</th>\n",
       "      <th>residual_sugar</th>\n",
       "      <th>chlorides</th>\n",
       "      <th>free_sulfur_dioxide</th>\n",
       "      <th>total_sulfur_dioxide</th>\n",
       "      <th>density</th>\n",
       "      <th>ph</th>\n",
       "      <th>sulphates</th>\n",
       "      <th>alcohol</th>\n",
       "      <th>quality</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>7.0</td>\n",
       "      <td>0.27</td>\n",
       "      <td>0.36</td>\n",
       "      <td>20.7</td>\n",
       "      <td>0.045</td>\n",
       "      <td>45.0</td>\n",
       "      <td>170.0</td>\n",
       "      <td>1.00100</td>\n",
       "      <td>3.00</td>\n",
       "      <td>0.45</td>\n",
       "      <td>8.800000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>6.3</td>\n",
       "      <td>0.30</td>\n",
       "      <td>0.34</td>\n",
       "      <td>1.6</td>\n",
       "      <td>0.049</td>\n",
       "      <td>14.0</td>\n",
       "      <td>132.0</td>\n",
       "      <td>0.99400</td>\n",
       "      <td>3.30</td>\n",
       "      <td>0.49</td>\n",
       "      <td>9.500000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>8.1</td>\n",
       "      <td>0.28</td>\n",
       "      <td>0.40</td>\n",
       "      <td>6.9</td>\n",
       "      <td>0.050</td>\n",
       "      <td>30.0</td>\n",
       "      <td>97.0</td>\n",
       "      <td>0.99510</td>\n",
       "      <td>3.26</td>\n",
       "      <td>0.44</td>\n",
       "      <td>10.100000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>7.2</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.32</td>\n",
       "      <td>8.5</td>\n",
       "      <td>0.058</td>\n",
       "      <td>47.0</td>\n",
       "      <td>186.0</td>\n",
       "      <td>0.99560</td>\n",
       "      <td>3.19</td>\n",
       "      <td>0.40</td>\n",
       "      <td>9.900000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>7.2</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.32</td>\n",
       "      <td>8.5</td>\n",
       "      <td>0.058</td>\n",
       "      <td>47.0</td>\n",
       "      <td>186.0</td>\n",
       "      <td>0.99560</td>\n",
       "      <td>3.19</td>\n",
       "      <td>0.40</td>\n",
       "      <td>9.900000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4851</th>\n",
       "      <td>6.4</td>\n",
       "      <td>0.33</td>\n",
       "      <td>0.44</td>\n",
       "      <td>8.9</td>\n",
       "      <td>0.055</td>\n",
       "      <td>52.0</td>\n",
       "      <td>164.0</td>\n",
       "      <td>0.99488</td>\n",
       "      <td>3.10</td>\n",
       "      <td>0.48</td>\n",
       "      <td>9.600000</td>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4855</th>\n",
       "      <td>7.1</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.39</td>\n",
       "      <td>13.7</td>\n",
       "      <td>0.058</td>\n",
       "      <td>26.0</td>\n",
       "      <td>172.0</td>\n",
       "      <td>0.99755</td>\n",
       "      <td>2.90</td>\n",
       "      <td>0.46</td>\n",
       "      <td>9.000000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4856</th>\n",
       "      <td>7.1</td>\n",
       "      <td>0.23</td>\n",
       "      <td>0.39</td>\n",
       "      <td>13.7</td>\n",
       "      <td>0.058</td>\n",
       "      <td>26.0</td>\n",
       "      <td>172.0</td>\n",
       "      <td>0.99755</td>\n",
       "      <td>2.90</td>\n",
       "      <td>0.46</td>\n",
       "      <td>9.000000</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4879</th>\n",
       "      <td>6.6</td>\n",
       "      <td>0.34</td>\n",
       "      <td>0.40</td>\n",
       "      <td>8.1</td>\n",
       "      <td>0.046</td>\n",
       "      <td>68.0</td>\n",
       "      <td>170.0</td>\n",
       "      <td>0.99494</td>\n",
       "      <td>3.15</td>\n",
       "      <td>0.50</td>\n",
       "      <td>9.533333</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4880</th>\n",
       "      <td>6.6</td>\n",
       "      <td>0.34</td>\n",
       "      <td>0.40</td>\n",
       "      <td>8.1</td>\n",
       "      <td>0.046</td>\n",
       "      <td>68.0</td>\n",
       "      <td>170.0</td>\n",
       "      <td>0.99494</td>\n",
       "      <td>3.15</td>\n",
       "      <td>0.50</td>\n",
       "      <td>9.533333</td>\n",
       "      <td>6</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>1709 rows × 12 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "      fixed_acidity  volatile_acidity  citric_acid  residual_sugar  chlorides  \\\n",
       "0               7.0              0.27         0.36            20.7      0.045   \n",
       "1               6.3              0.30         0.34             1.6      0.049   \n",
       "2               8.1              0.28         0.40             6.9      0.050   \n",
       "3               7.2              0.23         0.32             8.5      0.058   \n",
       "4               7.2              0.23         0.32             8.5      0.058   \n",
       "...             ...               ...          ...             ...        ...   \n",
       "4851            6.4              0.33         0.44             8.9      0.055   \n",
       "4855            7.1              0.23         0.39            13.7      0.058   \n",
       "4856            7.1              0.23         0.39            13.7      0.058   \n",
       "4879            6.6              0.34         0.40             8.1      0.046   \n",
       "4880            6.6              0.34         0.40             8.1      0.046   \n",
       "\n",
       "      free_sulfur_dioxide  total_sulfur_dioxide  density    ph  sulphates  \\\n",
       "0                    45.0                 170.0  1.00100  3.00       0.45   \n",
       "1                    14.0                 132.0  0.99400  3.30       0.49   \n",
       "2                    30.0                  97.0  0.99510  3.26       0.44   \n",
       "3                    47.0                 186.0  0.99560  3.19       0.40   \n",
       "4                    47.0                 186.0  0.99560  3.19       0.40   \n",
       "...                   ...                   ...      ...   ...        ...   \n",
       "4851                 52.0                 164.0  0.99488  3.10       0.48   \n",
       "4855                 26.0                 172.0  0.99755  2.90       0.46   \n",
       "4856                 26.0                 172.0  0.99755  2.90       0.46   \n",
       "4879                 68.0                 170.0  0.99494  3.15       0.50   \n",
       "4880                 68.0                 170.0  0.99494  3.15       0.50   \n",
       "\n",
       "        alcohol  quality  \n",
       "0      8.800000        6  \n",
       "1      9.500000        6  \n",
       "2     10.100000        6  \n",
       "3      9.900000        6  \n",
       "4      9.900000        6  \n",
       "...         ...      ...  \n",
       "4851   9.600000        5  \n",
       "4855   9.000000        6  \n",
       "4856   9.000000        6  \n",
       "4879   9.533333        6  \n",
       "4880   9.533333        6  \n",
       "\n",
       "[1709 rows x 12 columns]"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine[wine.duplicated(subset=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',\n",
    "       'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',\n",
    "       'ph', 'sulphates', 'alcohol','quality'],keep=False)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "ad6d2dcf",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:18.854035Z",
     "iopub.status.busy": "2023-08-20T11:07:18.853301Z",
     "iopub.status.idle": "2023-08-20T11:07:18.861075Z",
     "shell.execute_reply": "2023-08-20T11:07:18.860170Z"
    },
    "papermill": {
     "duration": 0.035088,
     "end_time": "2023-08-20T11:07:18.864151",
     "exception": false,
     "start_time": "2023-08-20T11:07:18.829063",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine.drop_duplicates(subset=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar',\n",
    "       'chlorides', 'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density',\n",
    "       'ph', 'sulphates', 'alcohol','quality'],keep='first',inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "2771cbcd",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.098362Z",
     "iopub.status.busy": "2023-08-20T11:07:19.097911Z",
     "iopub.status.idle": "2023-08-20T11:07:19.120200Z",
     "shell.execute_reply": "2023-08-20T11:07:19.119047Z"
    },
    "papermill": {
     "duration": 0.050353,
     "end_time": "2023-08-20T11:07:19.122867",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.072514",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Int64Index: 3961 entries, 0 to 4897\n",
      "Data columns (total 12 columns):\n",
      " #   Column                Non-Null Count  Dtype  \n",
      "---  ------                --------------  -----  \n",
      " 0   fixed_acidity         3961 non-null   float64\n",
      " 1   volatile_acidity      3961 non-null   float64\n",
      " 2   citric_acid           3961 non-null   float64\n",
      " 3   residual_sugar        3961 non-null   float64\n",
      " 4   chlorides             3961 non-null   float64\n",
      " 5   free_sulfur_dioxide   3961 non-null   float64\n",
      " 6   total_sulfur_dioxide  3961 non-null   float64\n",
      " 7   density               3961 non-null   float64\n",
      " 8   ph                    3961 non-null   float64\n",
      " 9   sulphates             3961 non-null   float64\n",
      " 10  alcohol               3961 non-null   float64\n",
      " 11  quality               3961 non-null   int64  \n",
      "dtypes: float64(11), int64(1)\n",
      "memory usage: 402.3 KB\n"
     ]
    }
   ],
   "source": [
    "wine.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "cf58cbd1",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.171508Z",
     "iopub.status.busy": "2023-08-20T11:07:19.171120Z",
     "iopub.status.idle": "2023-08-20T11:07:19.226047Z",
     "shell.execute_reply": "2023-08-20T11:07:19.225167Z"
    },
    "papermill": {
     "duration": 0.082115,
     "end_time": "2023-08-20T11:07:19.228274",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.146159",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>fixed_acidity</th>\n",
       "      <th>volatile_acidity</th>\n",
       "      <th>citric_acid</th>\n",
       "      <th>residual_sugar</th>\n",
       "      <th>chlorides</th>\n",
       "      <th>free_sulfur_dioxide</th>\n",
       "      <th>total_sulfur_dioxide</th>\n",
       "      <th>density</th>\n",
       "      <th>ph</th>\n",
       "      <th>sulphates</th>\n",
       "      <th>alcohol</th>\n",
       "      <th>quality</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>count</th>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "      <td>3961.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>mean</th>\n",
       "      <td>6.839346</td>\n",
       "      <td>0.280538</td>\n",
       "      <td>0.334332</td>\n",
       "      <td>5.914819</td>\n",
       "      <td>0.045905</td>\n",
       "      <td>34.889169</td>\n",
       "      <td>137.193512</td>\n",
       "      <td>0.993790</td>\n",
       "      <td>3.195458</td>\n",
       "      <td>0.490351</td>\n",
       "      <td>10.589358</td>\n",
       "      <td>5.854835</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>std</th>\n",
       "      <td>0.866860</td>\n",
       "      <td>0.103437</td>\n",
       "      <td>0.122446</td>\n",
       "      <td>4.861646</td>\n",
       "      <td>0.023103</td>\n",
       "      <td>17.210021</td>\n",
       "      <td>43.129065</td>\n",
       "      <td>0.002905</td>\n",
       "      <td>0.151546</td>\n",
       "      <td>0.113523</td>\n",
       "      <td>1.217076</td>\n",
       "      <td>0.890683</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>min</th>\n",
       "      <td>3.800000</td>\n",
       "      <td>0.080000</td>\n",
       "      <td>0.000000</td>\n",
       "      <td>0.600000</td>\n",
       "      <td>0.009000</td>\n",
       "      <td>2.000000</td>\n",
       "      <td>9.000000</td>\n",
       "      <td>0.987110</td>\n",
       "      <td>2.720000</td>\n",
       "      <td>0.220000</td>\n",
       "      <td>8.000000</td>\n",
       "      <td>3.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>25%</th>\n",
       "      <td>6.300000</td>\n",
       "      <td>0.210000</td>\n",
       "      <td>0.270000</td>\n",
       "      <td>1.600000</td>\n",
       "      <td>0.035000</td>\n",
       "      <td>23.000000</td>\n",
       "      <td>106.000000</td>\n",
       "      <td>0.991620</td>\n",
       "      <td>3.090000</td>\n",
       "      <td>0.410000</td>\n",
       "      <td>9.500000</td>\n",
       "      <td>5.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>50%</th>\n",
       "      <td>6.800000</td>\n",
       "      <td>0.260000</td>\n",
       "      <td>0.320000</td>\n",
       "      <td>4.700000</td>\n",
       "      <td>0.042000</td>\n",
       "      <td>33.000000</td>\n",
       "      <td>133.000000</td>\n",
       "      <td>0.993500</td>\n",
       "      <td>3.180000</td>\n",
       "      <td>0.480000</td>\n",
       "      <td>10.400000</td>\n",
       "      <td>6.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>75%</th>\n",
       "      <td>7.300000</td>\n",
       "      <td>0.330000</td>\n",
       "      <td>0.390000</td>\n",
       "      <td>8.900000</td>\n",
       "      <td>0.050000</td>\n",
       "      <td>45.000000</td>\n",
       "      <td>166.000000</td>\n",
       "      <td>0.995710</td>\n",
       "      <td>3.290000</td>\n",
       "      <td>0.550000</td>\n",
       "      <td>11.400000</td>\n",
       "      <td>6.000000</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>max</th>\n",
       "      <td>14.200000</td>\n",
       "      <td>1.100000</td>\n",
       "      <td>1.660000</td>\n",
       "      <td>65.800000</td>\n",
       "      <td>0.346000</td>\n",
       "      <td>289.000000</td>\n",
       "      <td>440.000000</td>\n",
       "      <td>1.038980</td>\n",
       "      <td>3.820000</td>\n",
       "      <td>1.080000</td>\n",
       "      <td>14.200000</td>\n",
       "      <td>9.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "       fixed_acidity  volatile_acidity  citric_acid  residual_sugar  \\\n",
       "count    3961.000000       3961.000000  3961.000000     3961.000000   \n",
       "mean        6.839346          0.280538     0.334332        5.914819   \n",
       "std         0.866860          0.103437     0.122446        4.861646   \n",
       "min         3.800000          0.080000     0.000000        0.600000   \n",
       "25%         6.300000          0.210000     0.270000        1.600000   \n",
       "50%         6.800000          0.260000     0.320000        4.700000   \n",
       "75%         7.300000          0.330000     0.390000        8.900000   \n",
       "max        14.200000          1.100000     1.660000       65.800000   \n",
       "\n",
       "         chlorides  free_sulfur_dioxide  total_sulfur_dioxide      density  \\\n",
       "count  3961.000000          3961.000000           3961.000000  3961.000000   \n",
       "mean      0.045905            34.889169            137.193512     0.993790   \n",
       "std       0.023103            17.210021             43.129065     0.002905   \n",
       "min       0.009000             2.000000              9.000000     0.987110   \n",
       "25%       0.035000            23.000000            106.000000     0.991620   \n",
       "50%       0.042000            33.000000            133.000000     0.993500   \n",
       "75%       0.050000            45.000000            166.000000     0.995710   \n",
       "max       0.346000           289.000000            440.000000     1.038980   \n",
       "\n",
       "                ph    sulphates      alcohol      quality  \n",
       "count  3961.000000  3961.000000  3961.000000  3961.000000  \n",
       "mean      3.195458     0.490351    10.589358     5.854835  \n",
       "std       0.151546     0.113523     1.217076     0.890683  \n",
       "min       2.720000     0.220000     8.000000     3.000000  \n",
       "25%       3.090000     0.410000     9.500000     5.000000  \n",
       "50%       3.180000     0.480000    10.400000     6.000000  \n",
       "75%       3.290000     0.550000    11.400000     6.000000  \n",
       "max       3.820000     1.080000    14.200000     9.000000  "
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine.describe()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "605911fc",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.278466Z",
     "iopub.status.busy": "2023-08-20T11:07:19.277250Z",
     "iopub.status.idle": "2023-08-20T11:07:19.554569Z",
     "shell.execute_reply": "2023-08-20T11:07:19.553380Z"
    },
    "papermill": {
     "duration": 0.30534,
     "end_time": "2023-08-20T11:07:19.557360",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.252020",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: xlabel='quality', ylabel='count'>"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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+fJt3bp1GTlyZJYsWZL77ruv1V1vb+fAAw9Mp06dsnjx4hx44IGpra3Nyy+/vNG8V155JTU1NZs8TlVVVaqqqt5zfgAAAADarzb9zre3irfFixdnzpw56dmz57vu8+STT2bdunWpq6tLkgwcODCNjY159NFHy3MeeeSRNDY2ZtCgQYVlBwAAAICK3vm2atWqPPfcc+X1JUuWZOHChenRo0fq6+vz93//93n88cfz4x//OOvXry+/o61Hjx7p3Llznn/++UyfPj3HH398evXqlaeeeirjx4/PAQcckMMOOyxJss8+++S4447LmDFjcv311ydJPv/5z2f48OG+dAoAAABAoUotLS0tlfrx+++/P0ceeeRG42eddVYmTZqUvn37vu1+P//5zzN48OC8+OKL+fSnP51FixZl1apVaWhoyAknnJCvfe1r6dGjR3n+H//4x1xwwQX54Q9/mCQZMWJEpk6dutFXU99JU1NTqqur09jY+K6PvgIA26e5hx9R6Qi0IUc8MLfSEQCACtmcnqii5du2RPkGACjf+HPKNwBovzanJ2rT73wDAAAAgG2Z8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKEjHSgcAgLdz2JTDKh2BNuSh8x+qdAQAANgi7nwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCBbVL4dddRRWbly5UbjTU1NOeqoo/7q4zzwwAM58cQTU19fn1KplLvuuqvV9paWlkyaNCn19fXp0qVLBg8enCeffLLVnObm5px//vnp1atXunbtmhEjRuSll15qNWfFihUZNWpUqqurU11dnVGjRr1tfgAAAADYmraofLv//vuzdu3ajcbfeOON/OIXv/irj7N69erst99+mTp16ttuv/LKK3P11Vdn6tSpWbBgQWpra3PMMcfktddeK88ZO3ZsZs6cmRkzZuTBBx/MqlWrMnz48Kxfv74854wzzsjChQsza9aszJo1KwsXLsyoUaM244wBAAAAYPN13JzJ//mf/1n++6mnnsqyZcvK6+vXr8+sWbPyN3/zN3/18YYNG5Zhw4a97baWlpZce+21ueSSS3LyyScnSW677bbU1NTku9/9br7whS+ksbExN910U+64444MGTIkSTJt2rQ0NDRkzpw5OfbYY/P0009n1qxZmT9/fg499NAkyY033piBAwfmmWeeyd577705/xIAAAAAwF9ts8q3/fffP6VSKaVS6W0fL+3SpUumTJmyVYItWbIky5Yty9ChQ8tjVVVVOeKIIzJv3rx84QtfyGOPPZZ169a1mlNfX59+/fpl3rx5OfbYY/Pwww+nurq6XLwlyYABA1JdXZ158+Yp3wAAAAAozGaVb0uWLElLS0t23333PProo9l1113L2zp37pzevXunQ4cOWyXYW3fV1dTUtBqvqanJ7373u/Kczp07Z5dddtlozlv7L1u2LL17997o+L179251595fam5uTnNzc3m9qalpy04EAAAAgHZrs8q3Pn36JEk2bNhQSJi3UyqVWq23tLRsNPaX/nLO281/t+NMnjw5l1122WamBQAAAID/sVnl25979tlnc//992f58uUblXFf/epX33Ow2traJH+6c62urq48vnz58vLdcLW1tVm7dm1WrFjR6u635cuXZ9CgQeU5L7/88kbHf+WVVza6q+7PTZw4MePGjSuvNzU1paGh4b2dFAAAAADtyhaVbzfeeGP+1//6X+nVq1dqa2s3ustsa5Rvffv2TW1tbWbPnp0DDjggSbJ27drMnTs33/zmN5MkBx10UDp16pTZs2dn5MiRSZKlS5dm0aJFufLKK5MkAwcOTGNjYx599NF87GMfS5I88sgjaWxsLBd0b6eqqipVVVXv+TwAAAAAaL+2qHy7/PLL841vfCMXXXTRe/rxVatW5bnnniuvL1myJAsXLkyPHj2y2267ZezYsbniiiuy5557Zs8998wVV1yRnXbaKWeccUaSpLq6OqNHj8748ePTs2fP9OjRIxMmTEj//v3LXz/dZ599ctxxx2XMmDG5/vrrkySf//znM3z4cB9bAAAAAKBQW1S+rVixIqeeeup7/vFf/vKXOfLII8vrbz3medZZZ+XWW2/NhRdemDVr1uTcc8/NihUrcuihh+bee+9Nt27dyvtcc8016dixY0aOHJk1a9bk6KOPzq233trqww/Tp0/PBRdcUP4q6ogRIzJ16tT3nB8AAAAA3kmppaWlZXN3Gj16dA455JD8wz/8QxGZ2qSmpqZUV1ensbEx3bt3r3QcgO3eYVMOq3QE2pCHzn+o0hGSJHMPP6LSEWhDjnhgbqUjAAAVsjk90Rbd+bbHHnvk0ksvzfz589O/f/906tSp1fYLLrhgSw4LAAAAANuVLSrfbrjhhuy8886ZO3du5s5t/f/4lUol5RsAAAAAZAvLtyVLlmztHAAAAACw3dmh0gEAAAAAYHu1RXe+nXPOOe+4/eabb96iMAAAAACwPdmi8m3FihWt1tetW5dFixZl5cqVOeqoo7ZKMAAAAADY1m1R+TZz5syNxjZs2JBzzz03u++++3sOBQAAAADbg632zrcddtghX/rSl3LNNddsrUMCAAAAwDZtq35w4fnnn8+bb765NQ8JAAAAANusLXrsdNy4ca3WW1pasnTp0tx9990566yztkowAAAAANjWbVH59qtf/arV+g477JBdd901V1111bt+CRUAAAAA2ostKt9+/vOfb+0cAAAAALDd2aLy7S2vvPJKnnnmmZRKpey1117Zddddt1YuAAAAANjmbdEHF1avXp1zzjkndXV1Ofzww/OJT3wi9fX1GT16dF5//fWtnREAAAAAtklbVL6NGzcuc+fOzY9+9KOsXLkyK1euzA9+8IPMnTs348eP39oZAQAAAGCbtEWPnf7Hf/xHvve972Xw4MHlseOPPz5dunTJyJEjc911122tfAAAAACwzdqiO99ef/311NTUbDTeu3dvj50CAAAAwP+zReXbwIED87WvfS1vvPFGeWzNmjW57LLLMnDgwK0WDgAAAAC2ZVv02Om1116bYcOG5YMf/GD222+/lEqlLFy4MFVVVbn33nu3dkYAAAAA2CZtUfnWv3//LF68ONOmTct//dd/paWlJaeffnrOPPPMdOnSZWtnBAAAAIBt0haVb5MnT05NTU3GjBnTavzmm2/OK6+8kosuumirhAMAAACAbdkWvfPt+uuvz0c+8pGNxvfdd9/8y7/8y3sOBQAAAADbgy0q35YtW5a6urqNxnfdddcsXbr0PYcCAAAAgO3BFpVvDQ0NeeihhzYaf+ihh1JfX/+eQwEAAADA9mCL3vn2uc99LmPHjs26dety1FFHJUl+9rOf5cILL8z48eO3akAAAAAA2FZtUfl24YUX5o9//GPOPffcrF27Nkmy44475qKLLsrEiRO3akAAAAAA2FZtUflWKpXyzW9+M5deemmefvrpdOnSJXvuuWeqqqq2dj4AAAAA2GZtUfn2lp133jmHHHLI1soCAAAAANuVLfrgAgAAAADw7pRvAAAAAFAQ5RsAAAAAFET5BgAAAAAFUb4BAAAAQEGUbwAAAABQEOUbAAAAABRE+QYAAAAABVG+AQAAAEBBlG8AAAAAUBDlGwAAAAAURPkGAAAAAAVRvgEAAABAQdp8+fahD30opVJpo+W8885Lkpx99tkbbRswYECrYzQ3N+f8889Pr1690rVr14wYMSIvvfRSJU4HAAAAgHakzZdvCxYsyNKlS8vL7NmzkySnnnpqec5xxx3Xas5PfvKTVscYO3ZsZs6cmRkzZuTBBx/MqlWrMnz48Kxfv/59PRcAAAAA2peOlQ7wbnbddddW6//0T/+UD3/4wzniiCPKY1VVVamtrX3b/RsbG3PTTTfljjvuyJAhQ5Ik06ZNS0NDQ+bMmZNjjz22uPAAAAAAtGtt/s63P7d27dpMmzYt55xzTkqlUnn8/vvvT+/evbPXXntlzJgxWb58eXnbY489lnXr1mXo0KHlsfr6+vTr1y/z5s3b5G81Nzenqamp1QIAAAAAm2ObKt/uuuuurFy5MmeffXZ5bNiwYZk+fXruu+++XHXVVVmwYEGOOuqoNDc3J0mWLVuWzp07Z5dddml1rJqamixbtmyTvzV58uRUV1eXl4aGhkLOCQAAAIDtV5t/7PTP3XTTTRk2bFjq6+vLY6eddlr57379+uXggw9Onz59cvfdd+fkk0/e5LFaWlpa3T33lyZOnJhx48aV15uamhRwAAAAAGyWbaZ8+93vfpc5c+bk+9///jvOq6urS58+fbJ48eIkSW1tbdauXZsVK1a0uvtt+fLlGTRo0CaPU1VVlaqqqq0THgAAAIB2aZt57PSWW25J7969c8IJJ7zjvFdffTUvvvhi6urqkiQHHXRQOnXqVP5KapIsXbo0ixYtesfyDQAAAADeq23izrcNGzbklltuyVlnnZWOHf8n8qpVqzJp0qSccsopqaury29/+9tcfPHF6dWrV0466aQkSXV1dUaPHp3x48enZ8+e6dGjRyZMmJD+/fuXv34KAAAAAEXYJsq3OXPm5IUXXsg555zTarxDhw554okncvvtt2flypWpq6vLkUcemTvvvDPdunUrz7vmmmvSsWPHjBw5MmvWrMnRRx+dW2+9NR06dHi/TwUAAACAdmSbKN+GDh2alpaWjca7dOmSe+65513333HHHTNlypRMmTKliHgAAAAA8La2mXe+AQAAAMC2RvkGAAAAAAVRvgEAAABAQZRvAAAAAFAQ5RsAAAAAFGSb+NopAADw9qaO/1GlI9DGfPGqEysdAYA/4843AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAK0qbLt0mTJqVUKrVaamtry9tbWloyadKk1NfXp0uXLhk8eHCefPLJVsdobm7O+eefn169eqVr164ZMWJEXnrppff7VAAAAABoh9p0+ZYk++67b5YuXVpennjiifK2K6+8MldffXWmTp2aBQsWpLa2Nsccc0xee+218pyxY8dm5syZmTFjRh588MGsWrUqw4cPz/r16ytxOgAAAAC0Ix0rHeDddOzYsdXdbm9paWnJtddem0suuSQnn3xykuS2225LTU1Nvvvd7+YLX/hCGhsbc9NNN+WOO+7IkCFDkiTTpk1LQ0ND5syZk2OPPfZ9PRcAAAAA2pc2f+fb4sWLU19fn759++b000/Pb37zmyTJkiVLsmzZsgwdOrQ8t6qqKkcccUTmzZuXJHnssceybt26VnPq6+vTr1+/8pxNaW5uTlNTU6sFAAAAADZHmy7fDj300Nx+++255557cuONN2bZsmUZNGhQXn311SxbtixJUlNT02qfmpqa8rZly5al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AABsr5RvAAAAAFAQ5RsAAAAAFET5BgAAAAAFUb7xvrjuuuvy0Y9+NN27d0/37t0zcODA/PSnP610LGhl8uTJKZVKGTt2bKWj0M5NmjQppVKp1VJbW1vpWJD//u//zqc//en07NkzO+20U/bff/889thjlY5FO/ahD31oo39elkqlnHfeeZWORjv25ptv5h//8R/Tt2/fdOnSJbvvvnu+/vWvZ8OGDZWORjv32muvZezYsenTp0+6dOmSQYMGZcGCBZWO1S50rHQA2ocPfvCD+ad/+qfsscceSZLbbrstn/zkJ/OrX/0q++67b4XTQbJgwYLccMMN+ehHP1rpKJAk2XfffTNnzpzyeocOHSqYBpIVK1bksMMOy5FHHpmf/vSn6d27d55//vl84AMfqHQ02rEFCxZk/fr15fVFixblmGOOyamnnlrBVLR33/zmN/Mv//Ivue2227Lvvvvml7/8ZT772c+muro6//t//+9Kx6Md+9znPpdFixbljjvuSH19faZNm5YhQ4bkqaeeyt/8zd9UOt52rdTS0tJS6RC0Tz169Mi3vvWtjB49utJRaOdWrVqVAw88MN/5zndy+eWXZ//998+1115b6Vi0Y5MmTcpdd92VhQsXVjoKlH3lK1/JQw89lF/84heVjgKbNHbs2Pz4xz/O4sWLUyqVKh2Hdmr48OGpqanJTTfdVB475ZRTstNOO+WOO+6oYDLaszVr1qRbt275wQ9+kBNOOKE8vv/++2f48OG5/PLLK5hu++exU95369evz4wZM7J69eoMHDiw0nEg5513Xk444YQMGTKk0lGgbPHixamvr0/fvn1z+umn5ze/+U2lI9HO/fCHP8zBBx+cU089Nb17984BBxyQG2+8sdKxoGzt2rWZNm1azjnnHMUbFfXxj388P/vZz/Lss88mSX7961/nwQcfzPHHH1/hZLRnb775ZtavX58dd9yx1XiXLl3y4IMPVihV++GxU943TzzxRAYOHJg33ngjO++8c2bOnJm//du/rXQs2rkZM2bk8ccf964D2pRDDz00t99+e/baa6+8/PLLufzyyzNo0KA8+eST6dmzZ6Xj0U795je/yXXXXZdx48bl4osvzqOPPpoLLrggVVVV+cxnPlPpeJC77rorK1euzNlnn13pKLRzF110URobG/ORj3wkHTp0yPr16/ONb3wjn/rUpyodjXasW7duGThwYP7P//k/2WeffVJTU5N/+7d/yyOPPJI999yz0vG2ex475X2zdu3avPDCC1m5cmX+4z/+I//6r/+auXPnKuComBdffDEHH3xw7r333uy3335JksGDB3vslDZn9erV+fCHP5wLL7ww48aNq3Qc2qnOnTvn4IMPzrx588pjF1xwQRYsWJCHH364gsngT4499th07tw5P/rRjyodhXZuxowZ+fKXv5xvfetb2XfffbNw4cKMHTs2V199dc4666xKx6Mde/7553POOefkgQceSIcOHXLggQdmr732yuOPP56nnnqq0vG2a8o3KmbIkCH58Ic/nOuvv77SUWin7rrrrpx00kmtXmS/fv36lEql7LDDDmlubvaSe9qMY445JnvssUeuu+66SkehnerTp0+OOeaY/Ou//mt57Lrrrsvll1+e//7v/65gMkh+97vfZffdd8/3v//9fPKTn6x0HNq5hoaGfOUrX2n11d3LL78806ZNy3/9139VMBn8yerVq9PU1JS6urqcdtppWbVqVe6+++5Kx9queeyUimlpaUlzc3OlY9COHX300XniiSdajX32s5/NRz7ykVx00UWKN9qM5ubmPP300/nEJz5R6Si0Y4cddlieeeaZVmPPPvts+vTpU6FE8D9uueWW9O7du9VLxKFSXn/99eywQ+vXq3fo0CEbNmyoUCJorWvXrunatWtWrFiRe+65J1deeWWlI233lG+8Ly6++OIMGzYsDQ0Nee211zJjxozcf//9mTVrVqWj0Y5169Yt/fr1azXWtWvX9OzZc6NxeD9NmDAhJ554YnbbbbcsX748l19+eZqamjyqQkV96UtfyqBBg3LFFVdk5MiRefTRR3PDDTfkhhtuqHQ02rkNGzbklltuyVlnnZWOHf3PGyrvxBNPzDe+8Y3stttu2XffffOrX/0qV199dc4555xKR6Odu+eee9LS0pK99947zz33XL785S9n7733zmc/+9lKR9vu+U8n3hcvv/xyRo0alaVLl6a6ujof/ehHM2vWrBxzzDGVjgbQ5rz00kv51Kc+lT/84Q/ZddddM2DAgMyfP98dRlTUIYcckpkzZ2bixIn5+te/nr59++baa6/NmWeeWelotHNz5szJCy+8oNigzZgyZUouvfTSnHvuuVm+fHnq6+vzhS98IV/96lcrHY12rrGxMRMnTsxLL72UHj165JRTTsk3vvGNdOrUqdLRtnve+QYAAAAABdnh3acAAAAAAFtC+QYAAAAABVG+AQAAAEBBlG8AAAAAUBDlGwAAAAAURPkGAAAAAAVRvgEAAABAQZRvAABssUmTJmX//fcvr5999tn5u7/7u4rlAQBoazpWOgAAANuPb3/722lpaSmvDx48OPvvv3+uvfbayoUCAKgg5RsAAFtNdXV1pSMAALQpHjsFANhOrV69Op/5zGey8847p66uLldddVUGDx6csWPHJklKpVLuuuuuVvt84AMfyK233lpev+iii7LXXntlp512yu67755LL70069at2+Rv/vljp2effXbmzp2bb3/72ymVSimVSlmyZEn22GOP/PM//3Or/RYtWpQddtghzz///NY4dQCANkP5BgCwnfryl7+cn//855k5c2buvffe3H///Xnsscc26xjdunXLrbfemqeeeirf/va3c+ONN+aaa675q/b99re/nYEDB2bMmDFZunRpli5dmt122y3nnHNObrnlllZzb7755nziE5/Ihz/84c3KBwDQ1infAAC2Q6tWrcpNN92Uf/7nf84xxxyT/v3757bbbsv69es36zj/+I//mEGDBuVDH/pQTjzxxIwfPz7//u///lftW11dnc6dO2ennXZKbW1tamtr06FDh3z2s5/NM888k0cffTRJsm7dukybNi3nnHPOZp8nAEBb551vAADboeeffz5r167NwIEDy2M9evTI3nvvvVnH+d73vpdrr702zz33XFatWpU333wz3bt3f0/Z6urqcsIJJ+Tmm2/Oxz72sfz4xz/OG2+8kVNPPfU9HRcAoC1y5xsAwHboz784uimlUmmjeX/+Prf58+fn9NNPz7Bhw/LjH/84v/rVr3LJJZdk7dq17znf5z73ucyYMSNr1qzJLbfcktNOOy077bTTez4uAEBb4843AIDt0B577JFOnTpl/vz52W233ZIkK1asyLPPPpsjjjgiSbLrrrtm6dKl5X0WL16c119/vbz+0EMPpU+fPrnkkkvKY7/73e82K0fnzp3f9lHX448/Pl27ds11112Xn/70p3nggQc267gAANsK5RsAwHZo5513zujRo/PlL385PXv2TE1NTS655JLssMP/PPhw1FFHZerUqRkwYEA2bNiQiy66KJ06dSpv32OPPfLCCy9kxowZOeSQQ3L33Xdn5syZm5XjQx/6UB555JH89re/zc4775wePXpkhx12SIcOHXL22Wdn4sSJ2WOPPVo9HgsAsD3x2CkAwHbqW9/6Vg4//PCMGDEiQ4YMycc//vEcdNBB5e1XXXVVGhoacvjhh+eMM87IhAkTWj36+clPfjJf+tKX8sUvfjH7779/5s2bl0svvXSzMkyYMCEdOnTI3/7t32bXXXfNCy+8UN42evTorF271ocWAIDtWqnlr3khCAAA24XBgwdn//33z7XXXlvpKHnooYcyePDgvPTSS6mpqal0HACAQnjsFACA91Vzc3NefPHFXHrppRk5cqTiDQDYrnnsFACA99W//du/Ze+9905jY2OuvPLKSscBACiUx04BAAAAoCDufAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICC/P+kSTuNI0PDSgAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 1500x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,5))\n",
    "sns.countplot(data=wine,x='quality')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "04e7d004",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.608572Z",
     "iopub.status.busy": "2023-08-20T11:07:19.607701Z",
     "iopub.status.idle": "2023-08-20T11:07:19.618953Z",
     "shell.execute_reply": "2023-08-20T11:07:19.617718Z"
    },
    "papermill": {
     "duration": 0.039801,
     "end_time": "2023-08-20T11:07:19.621566",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.581765",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>quality</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>1788</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>1175</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>689</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>153</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>131</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>20</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>5</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   quality\n",
       "6     1788\n",
       "5     1175\n",
       "7      689\n",
       "4      153\n",
       "8      131\n",
       "3       20\n",
       "9        5"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine['quality'].value_counts().to_frame()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "801230e2",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.672646Z",
     "iopub.status.busy": "2023-08-20T11:07:19.671841Z",
     "iopub.status.idle": "2023-08-20T11:07:19.916252Z",
     "shell.execute_reply": "2023-08-20T11:07:19.915030Z"
    },
    "papermill": {
     "duration": 0.272775,
     "end_time": "2023-08-20T11:07:19.918959",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.646184",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: xlabel='quality', ylabel='count'>"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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+fJt3bp1GTlyZJYsWZL77ruv1V1vb+fAAw9Mp06dsnjx4hx44IGpra3Nyy+/vNG8V155JTU1NZs8TlVVVaqqqt5zfgAAAADarzb9zre3irfFixdnzpw56dmz57vu8+STT2bdunWpq6tLkgwcODCNjY159NFHy3MeeeSRNDY2ZtCgQYVlBwAAAICK3vm2atWqPPfcc+X1JUuWZOHChenRo0fq6+vz93//93n88cfz4x//OOvXry+/o61Hjx7p3Llznn/++UyfPj3HH398evXqlaeeeirjx4/PAQcckMMOOyxJss8+++S4447LmDFjcv311ydJPv/5z2f48OG+dAoAAABAoUotLS0tlfrx+++/P0ceeeRG42eddVYmTZqUvn37vu1+P//5zzN48OC8+OKL+fSnP51FixZl1apVaWhoyAknnJCvfe1r6dGjR3n+H//4x1xwwQX54Q9/mCQZMWJEpk6dutFXU99JU1NTqqur09jY+K6PvgIA26e5hx9R6Qi0IUc8MLfSEQCACtmcnqii5du2RPkGACjf+HPKNwBovzanJ2rT73wDAAAAgG2Z8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKEjHSgcAgLdz2JTDKh2BNuSh8x+qdAQAANgi7nwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCBbVL4dddRRWbly5UbjTU1NOeqoo/7q4zzwwAM58cQTU19fn1KplLvuuqvV9paWlkyaNCn19fXp0qVLBg8enCeffLLVnObm5px//vnp1atXunbtmhEjRuSll15qNWfFihUZNWpUqqurU11dnVGjRr1tfgAAAADYmraofLv//vuzdu3ajcbfeOON/OIXv/irj7N69erst99+mTp16ttuv/LKK3P11Vdn6tSpWbBgQWpra3PMMcfktddeK88ZO3ZsZs6cmRkzZuTBBx/MqlWrMnz48Kxfv74854wzzsjChQsza9aszJo1KwsXLsyoUaM244wBAAAAYPN13JzJ//mf/1n++6mnnsqyZcvK6+vXr8+sWbPyN3/zN3/18YYNG5Zhw4a97baWlpZce+21ueSSS3LyyScnSW677bbU1NTku9/9br7whS+ksbExN910U+64444MGTIkSTJt2rQ0NDRkzpw5OfbYY/P0009n1qxZmT9/fg499NAkyY033piBAwfmmWeeyd577705/xIAAAAAwF9ts8q3/fffP6VSKaVS6W0fL+3SpUumTJmyVYItWbIky5Yty9ChQ8tjVVVVOeKIIzJv3rx84QtfyGOPPZZ169a1mlNfX59+/fpl3rx5OfbYY/Pwww+nurq6XLwlyYABA1JdXZ158+Yp3wAAAAAozGaVb0uWLElLS0t23333PProo9l1113L2zp37pzevXunQ4cOWyXYW3fV1dTUtBqvqanJ7373u/Kczp07Z5dddtlozlv7L1u2LL17997o+L179251595fam5uTnNzc3m9qalpy04EAAAAgHZrs8q3Pn36JEk2bNhQSJi3UyqVWq23tLRsNPaX/nLO281/t+NMnjw5l1122WamBQAAAID/sVnl25979tlnc//992f58uUblXFf/epX33Ow2traJH+6c62urq48vnz58vLdcLW1tVm7dm1WrFjR6u635cuXZ9CgQeU5L7/88kbHf+WVVza6q+7PTZw4MePGjSuvNzU1paGh4b2dFAAAAADtyhaVbzfeeGP+1//6X+nVq1dqa2s3ustsa5Rvffv2TW1tbWbPnp0DDjggSbJ27drMnTs33/zmN5MkBx10UDp16pTZs2dn5MiRSZKlS5dm0aJFufLKK5MkAwcOTGNjYx599NF87GMfS5I88sgjaWxsLBd0b6eqqipVVVXv+TwAAAAAaL+2qHy7/PLL841vfCMXXXTRe/rxVatW5bnnniuvL1myJAsXLkyPHj2y2267ZezYsbniiiuy5557Zs8998wVV1yRnXbaKWeccUaSpLq6OqNHj8748ePTs2fP9OjRIxMmTEj//v3LXz/dZ599ctxxx2XMmDG5/vrrkySf//znM3z4cB9bAAAAAKBQW1S+rVixIqeeeup7/vFf/vKXOfLII8vrbz3medZZZ+XWW2/NhRdemDVr1uTcc8/NihUrcuihh+bee+9Nt27dyvtcc8016dixY0aOHJk1a9bk6KOPzq233trqww/Tp0/PBRdcUP4q6ogRIzJ16tT3nB8AAAAA3kmppaWlZXN3Gj16dA455JD8wz/8QxGZ2qSmpqZUV1ensbEx3bt3r3QcgO3eYVMOq3QE2pCHzn+o0hGSJHMPP6LSEWhDjnhgbqUjAAAVsjk90Rbd+bbHHnvk0ksvzfz589O/f/906tSp1fYLLrhgSw4LAAAAANuVLSrfbrjhhuy8886ZO3du5s5t/f/4lUol5RsAAAAAZAvLtyVLlmztHAAAAACw3dmh0gEAAAAAYHu1RXe+nXPOOe+4/eabb96iMAAAAACwPdmi8m3FihWt1tetW5dFixZl5cqVOeqoo7ZKMAAAAADY1m1R+TZz5syNxjZs2JBzzz03u++++3sOBQAAAADbg632zrcddtghX/rSl3LNNddsrUMCAAAAwDZtq35w4fnnn8+bb765NQ8JAAAAANusLXrsdNy4ca3WW1pasnTp0tx9990566yztkowAAAAANjWbVH59qtf/arV+g477JBdd901V1111bt+CRUAAAAA2ostKt9+/vOfb+0cAAAAALDd2aLy7S2vvPJKnnnmmZRKpey1117Zddddt1YuAAAAANjmbdEHF1avXp1zzjkndXV1Ofzww/OJT3wi9fX1GT16dF5//fWtnREAAAAAtklbVL6NGzcuc+fOzY9+9KOsXLkyK1euzA9+8IPMnTs348eP39oZAQAAAGCbtEWPnf7Hf/xHvve972Xw4MHlseOPPz5dunTJyJEjc911122tfAAAAACwzdqiO99ef/311NTUbDTeu3dvj50CAAAAwP+zReXbwIED87WvfS1vvPFGeWzNmjW57LLLMnDgwK0WDgAAAAC2ZVv02Om1116bYcOG5YMf/GD222+/lEqlLFy4MFVVVbn33nu3dkYAAAAA2CZtUfnWv3//LF68ONOmTct//dd/paWlJaeffnrOPPPMdOnSZWtnBAAAAIBt0haVb5MnT05NTU3GjBnTavzmm2/OK6+8kosuumirhAMAAACAbdkWvfPt+uuvz0c+8pGNxvfdd9/8y7/8y3sOBQAAAADbgy0q35YtW5a6urqNxnfdddcsXbr0PYcCAAAAgO3BFpVvDQ0NeeihhzYaf+ihh1JfX/+eQwEAAADA9mCL3vn2uc99LmPHjs26dety1FFHJUl+9rOf5cILL8z48eO3akAAAAAA2FZtUfl24YUX5o9//GPOPffcrF27Nkmy44475qKLLsrEiRO3akAAAAAA2FZtUflWKpXyzW9+M5deemmefvrpdOnSJXvuuWeqqqq2dj4AAAAA2GZtUfn2lp133jmHHHLI1soCAAAAANuVLfrgAgAAAADw7pRvAAAAAFAQ5RsAAAAAFET5BgAAAAAFUb4BAAAAQEGUbwAAAABQEOUbAAAAABRE+QYAAAAABVG+AQAAAEBBlG8AAAAAUBDlGwAAAAAURPkGAAAAAAVRvgEAAABAQdp8+fahD30opVJpo+W8885Lkpx99tkbbRswYECrYzQ3N+f8889Pr1690rVr14wYMSIvvfRSJU4HAAAAgHakzZdvCxYsyNKlS8vL7NmzkySnnnpqec5xxx3Xas5PfvKTVscYO3ZsZs6cmRkzZuTBBx/MqlWrMnz48Kxfv/59PRcAAAAA2peOlQ7wbnbddddW6//0T/+UD3/4wzniiCPKY1VVVamtrX3b/RsbG3PTTTfljjvuyJAhQ5Ik06ZNS0NDQ+bMmZNjjz22uPAAAAAAtGtt/s63P7d27dpMmzYt55xzTkqlUnn8/vvvT+/evbPXXntlzJgxWb58eXnbY489lnXr1mXo0KHlsfr6+vTr1y/z5s3b5G81Nzenqamp1QIAAAAAm2ObKt/uuuuurFy5MmeffXZ5bNiwYZk+fXruu+++XHXVVVmwYEGOOuqoNDc3J0mWLVuWzp07Z5dddml1rJqamixbtmyTvzV58uRUV1eXl4aGhkLOCQAAAIDtV5t/7PTP3XTTTRk2bFjq6+vLY6eddlr57379+uXggw9Onz59cvfdd+fkk0/e5LFaWlpa3T33lyZOnJhx48aV15uamhRwAAAAAGyWbaZ8+93vfpc5c+bk+9///jvOq6urS58+fbJ48eIkSW1tbdauXZsVK1a0uvtt+fLlGTRo0CaPU1VVlaqqqq0THgAAAIB2aZt57PSWW25J7969c8IJJ7zjvFdffTUvvvhi6urqkiQHHXRQOnXqVP5KapIsXbo0ixYtesfyDQAAAADeq23izrcNGzbklltuyVlnnZWOHf8n8qpVqzJp0qSccsopqaury29/+9tcfPHF6dWrV0466aQkSXV1dUaPHp3x48enZ8+e6dGjRyZMmJD+/fuXv34KAAAAAEXYJsq3OXPm5IUXXsg555zTarxDhw554okncvvtt2flypWpq6vLkUcemTvvvDPdunUrz7vmmmvSsWPHjBw5MmvWrMnRRx+dW2+9NR06dHi/TwUAAACAdmSbKN+GDh2alpaWjca7dOmSe+65513333HHHTNlypRMmTKliHgAAAAA8La2mXe+AQAAAMC2RvkGAAAAAAVRvgEAAABAQZRvAAAAAFAQ5RsAAAAAFGSb+NopAADw9qaO/1GlI9DGfPGqEysdAYA/4843AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICCKN8AAAAAoCDKNwAAAAAoiPINAAAAAAqifAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAK0qbLt0mTJqVUKrVaamtry9tbWloyadKk1NfXp0uXLhk8eHCefPLJVsdobm7O+eefn169eqVr164ZMWJEXnrppff7VAAAAABoh9p0+ZYk++67b5YuXVpennjiifK2K6+8MldffXWmTp2aBQsWpLa2Nsccc0xee+218pyxY8dm5syZmTFjRh588MGsWrUqw4cPz/r16ytxOgAAAAC0Ix0rHeDddOzYsdXdbm9paWnJtddem0suuSQnn3xykuS2225LTU1Nvvvd7+YLX/hCGhsbc9NNN+WOO+7IkCFDkiTTpk1LQ0ND5syZk2OPPfZ9PRcAAAAA2pc2f+fb4sWLU19fn759++b000/Pb37zmyTJkiVLsmzZsgwdOrQ8t6qqKkcccUTmzZuXJHnssceybt26VnPq6+vTr1+/8pxNaW5uTlNTU6sFAAAAADZHmy7fDj300Nx+++255557cuONN2bZsmUZNGhQXn311SxbtixJUlNT02qfmpqa8rZly5al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AABsr5RvAAAAAFAQ5RsAAAAAFET5BgAAAAAFUb7xvrjuuuvy0Y9+NN27d0/37t0zcODA/PSnP610LGhl8uTJKZVKGTt2bKWj0M5NmjQppVKp1VJbW1vpWJD//u//zqc//en07NkzO+20U/bff/889thjlY5FO/ahD31oo39elkqlnHfeeZWORjv25ptv5h//8R/Tt2/fdOnSJbvvvnu+/vWvZ8OGDZWORjv32muvZezYsenTp0+6dOmSQYMGZcGCBZWO1S50rHQA2ocPfvCD+ad/+qfsscceSZLbbrstn/zkJ/OrX/0q++67b4XTQbJgwYLccMMN+ehHP1rpKJAk2XfffTNnzpzyeocOHSqYBpIVK1bksMMOy5FHHpmf/vSn6d27d55//vl84AMfqHQ02rEFCxZk/fr15fVFixblmGOOyamnnlrBVLR33/zmN/Mv//Ivue2227Lvvvvml7/8ZT772c+muro6//t//+9Kx6Md+9znPpdFixbljjvuSH19faZNm5YhQ4bkqaeeyt/8zd9UOt52rdTS0tJS6RC0Tz169Mi3vvWtjB49utJRaOdWrVqVAw88MN/5zndy+eWXZ//998+1115b6Vi0Y5MmTcpdd92VhQsXVjoKlH3lK1/JQw89lF/84heVjgKbNHbs2Pz4xz/O4sWLUyqVKh2Hdmr48OGpqanJTTfdVB475ZRTstNOO+WOO+6oYDLaszVr1qRbt275wQ9+kBNOOKE8vv/++2f48OG5/PLLK5hu++exU95369evz4wZM7J69eoMHDiw0nEg5513Xk444YQMGTKk0lGgbPHixamvr0/fvn1z+umn5ze/+U2lI9HO/fCHP8zBBx+cU089Nb17984BBxyQG2+8sdKxoGzt2rWZNm1azjnnHMUbFfXxj388P/vZz/Lss88mSX7961/nwQcfzPHHH1/hZLRnb775ZtavX58dd9yx1XiXLl3y4IMPVihV++GxU943TzzxRAYOHJg33ngjO++8c2bOnJm//du/rXQs2rkZM2bk8ccf964D2pRDDz00t99+e/baa6+8/PLLufzyyzNo0KA8+eST6dmzZ6Xj0U795je/yXXXXZdx48bl4osvzqOPPpoLLrggVVVV+cxnPlPpeJC77rorK1euzNlnn13pKLRzF110URobG/ORj3wkHTp0yPr16/ONb3wjn/rUpyodjXasW7duGThwYP7P//k/2WeffVJTU5N/+7d/yyOPPJI999yz0vG2ex475X2zdu3avPDCC1m5cmX+4z/+I//6r/+auXPnKuComBdffDEHH3xw7r333uy3335JksGDB3vslDZn9erV+fCHP5wLL7ww48aNq3Qc2qnOnTvn4IMPzrx588pjF1xwQRYsWJCHH364gsngT4499th07tw5P/rRjyodhXZuxowZ+fKXv5xvfetb2XfffbNw4cKMHTs2V199dc4666xKx6Mde/7553POOefkgQceSIcOHXLggQdmr732yuOPP56nnnqq0vG2a8o3KmbIkCH58Ic/nOuvv77SUWin7rrrrpx00kmtXmS/fv36lEql7LDDDmlubvaSe9qMY445JnvssUeuu+66SkehnerTp0+OOeaY/Ou//mt57Lrrrsvll1+e//7v/65gMkh+97vfZffdd8/3v//9fPKTn6x0HNq5hoaGfOUrX2n11d3LL78806ZNy3/9139VMBn8yerVq9PU1JS6urqcdtppWbVqVe6+++5Kx9queeyUimlpaUlzc3OlY9COHX300XniiSdajX32s5/NRz7ykVx00UWKN9qM5ubmPP300/nEJz5R6Si0Y4cddlieeeaZVmPPPvts+vTpU6FE8D9uueWW9O7du9VLxKFSXn/99eywQ+vXq3fo0CEbNmyoUCJorWvXrunatWtWrFiRe+65J1deeWWlI233lG+8Ly6++OIMGzYsDQ0Nee211zJjxozcf//9mTVrVqWj0Y5169Yt/fr1azXWtWvX9OzZc6NxeD9NmDAhJ554YnbbbbcsX748l19+eZqamjyqQkV96UtfyqBBg3LFFVdk5MiRefTRR3PDDTfkhhtuqHQ02rkNGzbklltuyVlnnZWOHf3PGyrvxBNPzDe+8Y3stttu2XffffOrX/0qV199dc4555xKR6Odu+eee9LS0pK99947zz33XL785S9n7733zmc/+9lKR9vu+U8n3hcvv/xyRo0alaVLl6a6ujof/ehHM2vWrBxzzDGVjgbQ5rz00kv51Kc+lT/84Q/ZddddM2DAgMyfP98dRlTUIYcckpkzZ2bixIn5+te/nr59++baa6/NmWeeWelotHNz5szJCy+8oNigzZgyZUouvfTSnHvuuVm+fHnq6+vzhS98IV/96lcrHY12rrGxMRMnTsxLL72UHj165JRTTsk3vvGNdOrUqdLRtnve+QYAAAAABdnh3acAAAAAAFtC+QYAAAAABVG+AQAAAEBBlG8AAAAAUBDlGwAAAAAURPkGAAAAAAVRvgEAAABAQZRvAABssUmTJmX//fcvr5999tn5u7/7u4rlAQBoazpWOgAAANuPb3/722lpaSmvDx48OPvvv3+uvfbayoUCAKgg5RsAAFtNdXV1pSMAALQpHjsFANhOrV69Op/5zGey8847p66uLldddVUGDx6csWPHJklKpVLuuuuuVvt84AMfyK233lpev+iii7LXXntlp512yu67755LL70069at2+Rv/vljp2effXbmzp2bb3/72ymVSimVSlmyZEn22GOP/PM//3Or/RYtWpQddtghzz///NY4dQCANkP5BgCwnfryl7+cn//855k5c2buvffe3H///Xnsscc26xjdunXLrbfemqeeeirf/va3c+ONN+aaa675q/b99re/nYEDB2bMmDFZunRpli5dmt122y3nnHNObrnlllZzb7755nziE5/Ihz/84c3KBwDQ1infAAC2Q6tWrcpNN92Uf/7nf84xxxyT/v3757bbbsv69es36zj/+I//mEGDBuVDH/pQTjzxxIwfPz7//u///lftW11dnc6dO2ennXZKbW1tamtr06FDh3z2s5/NM888k0cffTRJsm7dukybNi3nnHPOZp8nAEBb551vAADboeeffz5r167NwIEDy2M9evTI3nvvvVnH+d73vpdrr702zz33XFatWpU333wz3bt3f0/Z6urqcsIJJ+Tmm2/Oxz72sfz4xz/OG2+8kVNPPfU9HRcAoC1y5xsAwHboz784uimlUmmjeX/+Prf58+fn9NNPz7Bhw/LjH/84v/rVr3LJJZdk7dq17znf5z73ucyYMSNr1qzJLbfcktNOOy077bTTez4uAEBb4843AIDt0B577JFOnTpl/vz52W233ZIkK1asyLPPPpsjjjgiSbLrrrtm6dKl5X0WL16c119/vbz+0EMPpU+fPrnkkkvKY7/73e82K0fnzp3f9lHX448/Pl27ds11112Xn/70p3nggQc267gAANsK5RsAwHZo5513zujRo/PlL385PXv2TE1NTS655JLssMP/PPhw1FFHZerUqRkwYEA2bNiQiy66KJ06dSpv32OPPfLCCy9kxowZOeSQQ3L33Xdn5syZm5XjQx/6UB555JH89re/zc4775wePXpkhx12SIcOHXL22Wdn4sSJ2WOPPVo9HgsAsD3x2CkAwHbqW9/6Vg4//PCMGDEiQ4YMycc//vEcdNBB5e1XXXVVGhoacvjhh+eMM87IhAkTWj36+clPfjJf+tKX8sUvfjH7779/5s2bl0svvXSzMkyYMCEdOnTI3/7t32bXXXfNCy+8UN42evTorF271ocWAIDtWqnlr3khCAAA24XBgwdn//33z7XXXlvpKHnooYcyePDgvPTSS6mpqal0HACAQnjsFACA91Vzc3NefPHFXHrppRk5cqTiDQDYrnnsFACA99W//du/Ze+9905jY2OuvPLKSscBACiUx04BAAAAoCDufAMAAACAgijfAAAAAKAgyjcAAAAAKIjyDQAAAAAKonwDAAAAgIIo3wAAAACgIMo3AAAAACiI8g0AAAAACqJ8AwAAAICC/P+kSTuNI0PDSgAAAABJRU5ErkJggg==",
      "text/plain": [
       "<Figure size 1500x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,5))\n",
    "sns.countplot(data=wine,x='quality')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "id": "cc6fab9a",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:19.970861Z",
     "iopub.status.busy": "2023-08-20T11:07:19.970410Z",
     "iopub.status.idle": "2023-08-20T11:07:19.997104Z",
     "shell.execute_reply": "2023-08-20T11:07:19.995914Z"
    },
    "papermill": {
     "duration": 0.055663,
     "end_time": "2023-08-20T11:07:19.999574",
     "exception": false,
     "start_time": "2023-08-20T11:07:19.943911",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>fixed_acidity</th>\n",
       "      <th>volatile_acidity</th>\n",
       "      <th>citric_acid</th>\n",
       "      <th>residual_sugar</th>\n",
       "      <th>chlorides</th>\n",
       "      <th>free_sulfur_dioxide</th>\n",
       "      <th>total_sulfur_dioxide</th>\n",
       "      <th>density</th>\n",
       "      <th>ph</th>\n",
       "      <th>sulphates</th>\n",
       "      <th>alcohol</th>\n",
       "      <th>quality</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>fixed_acidity</th>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.019214</td>\n",
       "      <td>0.298959</td>\n",
       "      <td>0.083620</td>\n",
       "      <td>0.024036</td>\n",
       "      <td>-0.058396</td>\n",
       "      <td>0.082425</td>\n",
       "      <td>0.266091</td>\n",
       "      <td>-0.431274</td>\n",
       "      <td>-0.017453</td>\n",
       "      <td>-0.110788</td>\n",
       "      <td>-0.124636</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>volatile_acidity</th>\n",
       "      <td>-0.019214</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.163228</td>\n",
       "      <td>0.098340</td>\n",
       "      <td>0.086287</td>\n",
       "      <td>-0.102471</td>\n",
       "      <td>0.102315</td>\n",
       "      <td>0.060603</td>\n",
       "      <td>-0.046954</td>\n",
       "      <td>-0.021150</td>\n",
       "      <td>0.046815</td>\n",
       "      <td>-0.190678</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>citric_acid</th>\n",
       "      <td>0.298959</td>\n",
       "      <td>-0.163228</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.106269</td>\n",
       "      <td>0.132590</td>\n",
       "      <td>0.091681</td>\n",
       "      <td>0.122845</td>\n",
       "      <td>0.160076</td>\n",
       "      <td>-0.183015</td>\n",
       "      <td>0.049442</td>\n",
       "      <td>-0.076514</td>\n",
       "      <td>0.007065</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>residual_sugar</th>\n",
       "      <td>0.083620</td>\n",
       "      <td>0.098340</td>\n",
       "      <td>0.106269</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.076091</td>\n",
       "      <td>0.306835</td>\n",
       "      <td>0.409583</td>\n",
       "      <td>0.820498</td>\n",
       "      <td>-0.165997</td>\n",
       "      <td>-0.020503</td>\n",
       "      <td>-0.398167</td>\n",
       "      <td>-0.117339</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>chlorides</th>\n",
       "      <td>0.024036</td>\n",
       "      <td>0.086287</td>\n",
       "      <td>0.132590</td>\n",
       "      <td>0.076091</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.101272</td>\n",
       "      <td>0.191145</td>\n",
       "      <td>0.253088</td>\n",
       "      <td>-0.090573</td>\n",
       "      <td>0.017871</td>\n",
       "      <td>-0.356928</td>\n",
       "      <td>-0.217739</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>free_sulfur_dioxide</th>\n",
       "      <td>-0.058396</td>\n",
       "      <td>-0.102471</td>\n",
       "      <td>0.091681</td>\n",
       "      <td>0.306835</td>\n",
       "      <td>0.101272</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.619437</td>\n",
       "      <td>0.294638</td>\n",
       "      <td>-0.007750</td>\n",
       "      <td>0.037932</td>\n",
       "      <td>-0.251768</td>\n",
       "      <td>0.010507</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>total_sulfur_dioxide</th>\n",
       "      <td>0.082425</td>\n",
       "      <td>0.102315</td>\n",
       "      <td>0.122845</td>\n",
       "      <td>0.409583</td>\n",
       "      <td>0.191145</td>\n",
       "      <td>0.619437</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.536868</td>\n",
       "      <td>0.008239</td>\n",
       "      <td>0.136544</td>\n",
       "      <td>-0.446643</td>\n",
       "      <td>-0.183356</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>density</th>\n",
       "      <td>0.266091</td>\n",
       "      <td>0.060603</td>\n",
       "      <td>0.160076</td>\n",
       "      <td>0.820498</td>\n",
       "      <td>0.253088</td>\n",
       "      <td>0.294638</td>\n",
       "      <td>0.536868</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.063734</td>\n",
       "      <td>0.082048</td>\n",
       "      <td>-0.760162</td>\n",
       "      <td>-0.337805</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>ph</th>\n",
       "      <td>-0.431274</td>\n",
       "      <td>-0.046954</td>\n",
       "      <td>-0.183015</td>\n",
       "      <td>-0.165997</td>\n",
       "      <td>-0.090573</td>\n",
       "      <td>-0.007750</td>\n",
       "      <td>0.008239</td>\n",
       "      <td>-0.063734</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.142353</td>\n",
       "      <td>0.093095</td>\n",
       "      <td>0.123829</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>sulphates</th>\n",
       "      <td>-0.017453</td>\n",
       "      <td>-0.021150</td>\n",
       "      <td>0.049442</td>\n",
       "      <td>-0.020503</td>\n",
       "      <td>0.017871</td>\n",
       "      <td>0.037932</td>\n",
       "      <td>0.136544</td>\n",
       "      <td>0.082048</td>\n",
       "      <td>0.142353</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>-0.022850</td>\n",
       "      <td>0.053200</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>alcohol</th>\n",
       "      <td>-0.110788</td>\n",
       "      <td>0.046815</td>\n",
       "      <td>-0.076514</td>\n",
       "      <td>-0.398167</td>\n",
       "      <td>-0.356928</td>\n",
       "      <td>-0.251768</td>\n",
       "      <td>-0.446643</td>\n",
       "      <td>-0.760162</td>\n",
       "      <td>0.093095</td>\n",
       "      <td>-0.022850</td>\n",
       "      <td>1.000000</td>\n",
       "      <td>0.462869</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>quality</th>\n",
       "      <td>-0.124636</td>\n",
       "      <td>-0.190678</td>\n",
       "      <td>0.007065</td>\n",
       "      <td>-0.117339</td>\n",
       "      <td>-0.217739</td>\n",
       "      <td>0.010507</td>\n",
       "      <td>-0.183356</td>\n",
       "      <td>-0.337805</td>\n",
       "      <td>0.123829</td>\n",
       "      <td>0.053200</td>\n",
       "      <td>0.462869</td>\n",
       "      <td>1.000000</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                      fixed_acidity  volatile_acidity  citric_acid  \\\n",
       "fixed_acidity              1.000000         -0.019214     0.298959   \n",
       "volatile_acidity          -0.019214          1.000000    -0.163228   \n",
       "citric_acid                0.298959         -0.163228     1.000000   \n",
       "residual_sugar             0.083620          0.098340     0.106269   \n",
       "chlorides                  0.024036          0.086287     0.132590   \n",
       "free_sulfur_dioxide       -0.058396         -0.102471     0.091681   \n",
       "total_sulfur_dioxide       0.082425          0.102315     0.122845   \n",
       "density                    0.266091          0.060603     0.160076   \n",
       "ph                        -0.431274         -0.046954    -0.183015   \n",
       "sulphates                 -0.017453         -0.021150     0.049442   \n",
       "alcohol                   -0.110788          0.046815    -0.076514   \n",
       "quality                   -0.124636         -0.190678     0.007065   \n",
       "\n",
       "                      residual_sugar  chlorides  free_sulfur_dioxide  \\\n",
       "fixed_acidity               0.083620   0.024036            -0.058396   \n",
       "volatile_acidity            0.098340   0.086287            -0.102471   \n",
       "citric_acid                 0.106269   0.132590             0.091681   \n",
       "residual_sugar              1.000000   0.076091             0.306835   \n",
       "chlorides                   0.076091   1.000000             0.101272   \n",
       "free_sulfur_dioxide         0.306835   0.101272             1.000000   \n",
       "total_sulfur_dioxide        0.409583   0.191145             0.619437   \n",
       "density                     0.820498   0.253088             0.294638   \n",
       "ph                         -0.165997  -0.090573            -0.007750   \n",
       "sulphates                  -0.020503   0.017871             0.037932   \n",
       "alcohol                    -0.398167  -0.356928            -0.251768   \n",
       "quality                    -0.117339  -0.217739             0.010507   \n",
       "\n",
       "                      total_sulfur_dioxide   density        ph  sulphates  \\\n",
       "fixed_acidity                     0.082425  0.266091 -0.431274  -0.017453   \n",
       "volatile_acidity                  0.102315  0.060603 -0.046954  -0.021150   \n",
       "citric_acid                       0.122845  0.160076 -0.183015   0.049442   \n",
       "residual_sugar                    0.409583  0.820498 -0.165997  -0.020503   \n",
       "chlorides                         0.191145  0.253088 -0.090573   0.017871   \n",
       "free_sulfur_dioxide               0.619437  0.294638 -0.007750   0.037932   \n",
       "total_sulfur_dioxide              1.000000  0.536868  0.008239   0.136544   \n",
       "density                           0.536868  1.000000 -0.063734   0.082048   \n",
       "ph                                0.008239 -0.063734  1.000000   0.142353   \n",
       "sulphates                         0.136544  0.082048  0.142353   1.000000   \n",
       "alcohol                          -0.446643 -0.760162  0.093095  -0.022850   \n",
       "quality                          -0.183356 -0.337805  0.123829   0.053200   \n",
       "\n",
       "                       alcohol   quality  \n",
       "fixed_acidity        -0.110788 -0.124636  \n",
       "volatile_acidity      0.046815 -0.190678  \n",
       "citric_acid          -0.076514  0.007065  \n",
       "residual_sugar       -0.398167 -0.117339  \n",
       "chlorides            -0.356928 -0.217739  \n",
       "free_sulfur_dioxide  -0.251768  0.010507  \n",
       "total_sulfur_dioxide -0.446643 -0.183356  \n",
       "density              -0.760162 -0.337805  \n",
       "ph                    0.093095  0.123829  \n",
       "sulphates            -0.022850  0.053200  \n",
       "alcohol               1.000000  0.462869  \n",
       "quality               0.462869  1.000000  "
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wine.corr()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "id": "662a0dc5",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:20.053311Z",
     "iopub.status.busy": "2023-08-20T11:07:20.052861Z",
     "iopub.status.idle": "2023-08-20T11:07:21.025899Z",
     "shell.execute_reply": "2023-08-20T11:07:21.024725Z"
    },
    "papermill": {
     "duration": 1.004129,
     "end_time": "2023-08-20T11:07:21.029756",
     "exception": false,
     "start_time": "2023-08-20T11:07:20.025627",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: title={'center': 'correlation b/w features'}>"
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1500x500 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,5))\n",
    "plt.title('correlation b/w features')\n",
    "sns.heatmap(wine.corr(),annot=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "a76b93da",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.089988Z",
     "iopub.status.busy": "2023-08-20T11:07:21.089554Z",
     "iopub.status.idle": "2023-08-20T11:07:21.096853Z",
     "shell.execute_reply": "2023-08-20T11:07:21.095679Z"
    },
    "papermill": {
     "duration": 0.040763,
     "end_time": "2023-08-20T11:07:21.099494",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.058731",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "wine_quality_corr=wine.corr()['quality'].to_frame()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "2753827f",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.158603Z",
     "iopub.status.busy": "2023-08-20T11:07:21.158207Z",
     "iopub.status.idle": "2023-08-20T11:07:21.552533Z",
     "shell.execute_reply": "2023-08-20T11:07:21.551292Z"
    },
    "papermill": {
     "duration": 0.42704,
     "end_time": "2023-08-20T11:07:21.555322",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.128282",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<Axes: title={'center': 'correlation of target feature with predictor features'}, xlabel='quality'>"
      ]
     },
     "execution_count": 20,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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",
      "text/plain": [
       "<Figure size 1500x500 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.figure(figsize=(15,5))\n",
    "plt.title('correlation of target feature with predictor features')\n",
    "sns.barplot(data=wine_quality_corr,y=wine_quality_corr.index,x='quality')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "d6ca6507",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.617770Z",
     "iopub.status.busy": "2023-08-20T11:07:21.617386Z",
     "iopub.status.idle": "2023-08-20T11:07:21.623496Z",
     "shell.execute_reply": "2023-08-20T11:07:21.622324Z"
    },
    "papermill": {
     "duration": 0.040657,
     "end_time": "2023-08-20T11:07:21.625981",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.585324",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "y=wine['quality']\n",
    "x=wine.drop(['quality'],axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "da9a24d9",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.686073Z",
     "iopub.status.busy": "2023-08-20T11:07:21.685625Z",
     "iopub.status.idle": "2023-08-20T11:07:21.822480Z",
     "shell.execute_reply": "2023-08-20T11:07:21.821360Z"
    },
    "papermill": {
     "duration": 0.170389,
     "end_time": "2023-08-20T11:07:21.825286",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.654897",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "from sklearn.model_selection import train_test_split"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "bfadbadb",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.885470Z",
     "iopub.status.busy": "2023-08-20T11:07:21.885037Z",
     "iopub.status.idle": "2023-08-20T11:07:21.893326Z",
     "shell.execute_reply": "2023-08-20T11:07:21.891929Z"
    },
    "papermill": {
     "duration": 0.041605,
     "end_time": "2023-08-20T11:07:21.895864",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.854259",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=42)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "ac4e5291",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:21.955521Z",
     "iopub.status.busy": "2023-08-20T11:07:21.954778Z",
     "iopub.status.idle": "2023-08-20T11:07:21.962215Z",
     "shell.execute_reply": "2023-08-20T11:07:21.961329Z"
    },
    "papermill": {
     "duration": 0.03992,
     "end_time": "2023-08-20T11:07:21.964557",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.924637",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((2772, 11), (1189, 11), (2772,), (1189,))"
      ]
     },
     "execution_count": 24,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "x_train.shape,x_test.shape,y_train.shape,y_test.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "c76a6906",
   "metadata": {},
   "outputs": [],
   "source": [
    "def evaluate(y,pred):\n",
    "    rmse =np.sqrt(mean_squared_error(y,pred))\n",
    "    mae = mean_absolute_error(y,pred)\n",
    "    r2 = r2_score(y,pred)\n",
    "    \n",
    "    return rmse,mae,r2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "4a9a62a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_metrics(y_true, y_pred, y_pred_prob):\n",
    "    from sklearn.metrics import accuracy_score,precision_score,recall_score,log_loss\n",
    "    acc = accuracy_score(y_true, y_pred)\n",
    "    prec = precision_score(y_true, y_pred)\n",
    "    recall = recall_score(y_true, y_pred)\n",
    "    entropy = log_loss(y_true, y_pred_prob)\n",
    "    return {'accuracy': round(acc, 2), 'precision': round(prec, 2), 'recall': round(recall, 2), 'entropy': round(entropy, 2)}"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "86bc9fbd",
   "metadata": {},
   "source": [
    "# Model NO- 1- Logistic Regression"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "a32f1ab6",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:22.024692Z",
     "iopub.status.busy": "2023-08-20T11:07:22.024320Z",
     "iopub.status.idle": "2023-08-20T11:07:22.123271Z",
     "shell.execute_reply": "2023-08-20T11:07:22.122166Z"
    },
    "papermill": {
     "duration": 0.132408,
     "end_time": "2023-08-20T11:07:22.126107",
     "exception": false,
     "start_time": "2023-08-20T11:07:21.993699",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "from sklearn.linear_model import LogisticRegression"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "8ea9fe16",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:22.187579Z",
     "iopub.status.busy": "2023-08-20T11:07:22.186509Z",
     "iopub.status.idle": "2023-08-20T11:07:22.191609Z",
     "shell.execute_reply": "2023-08-20T11:07:22.190774Z"
    },
    "papermill": {
     "duration": 0.037975,
     "end_time": "2023-08-20T11:07:22.193865",
     "exception": false,
     "start_time": "2023-08-20T11:07:22.155890",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "lr=LogisticRegression(max_iter=6000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "1fb3f0a1",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:22.257585Z",
     "iopub.status.busy": "2023-08-20T11:07:22.256314Z",
     "iopub.status.idle": "2023-08-20T11:07:24.947668Z",
     "shell.execute_reply": "2023-08-20T11:07:24.946428Z"
    },
    "papermill": {
     "duration": 2.724342,
     "end_time": "2023-08-20T11:07:24.950374",
     "exception": false,
     "start_time": "2023-08-20T11:07:22.226032",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\naveen\\anaconda3\\Lib\\site-packages\\sklearn\\linear_model\\_logistic.py:458: ConvergenceWarning: lbfgs failed to converge (status=1):\n",
      "STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.\n",
      "\n",
      "Increase the number of iterations (max_iter) or scale the data as shown in:\n",
      "    https://scikit-learn.org/stable/modules/preprocessing.html\n",
      "Please also refer to the documentation for alternative solver options:\n",
      "    https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression\n",
      "  n_iter_i = _check_optimize_result(\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {color: black;background-color: white;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>LogisticRegression(max_iter=6000)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">LogisticRegression</label><div class=\"sk-toggleable__content\"><pre>LogisticRegression(max_iter=6000)</pre></div></div></div></div></div>"
      ],
      "text/plain": [
       "LogisticRegression(max_iter=6000)"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr.fit(x_train,y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "a29f19c9",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:25.012437Z",
     "iopub.status.busy": "2023-08-20T11:07:25.011988Z",
     "iopub.status.idle": "2023-08-20T11:07:25.022374Z",
     "shell.execute_reply": "2023-08-20T11:07:25.021501Z"
    },
    "papermill": {
     "duration": 0.044043,
     "end_time": "2023-08-20T11:07:25.024710",
     "exception": false,
     "start_time": "2023-08-20T11:07:24.980667",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.5494227994227994"
      ]
     },
     "execution_count": 30,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr.score(x_train,y_train)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "60ab638f",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:25.087556Z",
     "iopub.status.busy": "2023-08-20T11:07:25.086860Z",
     "iopub.status.idle": "2023-08-20T11:07:25.096757Z",
     "shell.execute_reply": "2023-08-20T11:07:25.095606Z"
    },
    "papermill": {
     "duration": 0.044379,
     "end_time": "2023-08-20T11:07:25.099537",
     "exception": false,
     "start_time": "2023-08-20T11:07:25.055158",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0.5332211942809083"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lr.score(x_test,y_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "26ff370d",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:25.162132Z",
     "iopub.status.busy": "2023-08-20T11:07:25.161625Z",
     "iopub.status.idle": "2023-08-20T11:07:25.168930Z",
     "shell.execute_reply": "2023-08-20T11:07:25.167684Z"
    },
    "papermill": {
     "duration": 0.041308,
     "end_time": "2023-08-20T11:07:25.171435",
     "exception": false,
     "start_time": "2023-08-20T11:07:25.130127",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "y_pred=lr.predict(x_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "562351c1",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\naveen\\anaconda3\\Lib\\site-packages\\_distutils_hack\\__init__.py:33: UserWarning: Setuptools is replacing distutils.\n",
      "  warnings.warn(\"Setuptools is replacing distutils.\")\n",
      "2023/09/11 16:14:31 WARNING mlflow.models.model: Logging model metadata to the tracking server has failed, possibly due older server version. The model artifacts have been logged successfully under mlflow-artifacts:/686109368148166702/a3478ce73e284ea69540d524dd4c25e6/artifacts. In addition to exporting model artifacts, MLflow clients 1.7.0 and above attempt to record model metadata to the tracking store. If logging to a mlflow server via REST, consider upgrading the server version to MLflow 1.7.0 or above. Set logging level to DEBUG via `logging.getLogger(\"mlflow\").setLevel(logging.DEBUG)` to see the full traceback.\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Logistic Regression Metrics:rmse:0.8304547985373997,mae:0.5349032800672834,r2:0.12609576394241961\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "#run = mlflow.start_run(run_name=\"My model experiment\")\n",
    " #mlflow.set_experiment(\"LOgistic Regression\")\n",
    "rmse,mae,r2 = evaluate(y_test,y_pred)\n",
    "mlflow.set_tag(\"developer\",\"Naveen\")\n",
    "mlflow.set_tag(\"Logistic_Reg\",\"Logistic_Regression\")\n",
    " #mlflow.log_params(params)\n",
    "mlflow.log_metric(\"rmse\",rmse)\n",
    "mlflow.log_metric(\"mae\",mae)\n",
    "mlflow.log_metric(\"r2\",r2)\n",
    "# mlflow.log_metric(\"Accuracy\",acc)                      \n",
    "mlflow.sklearn.log_model(lr,\"Logistic Regression\")\n",
    "print(f\"Logistic Regression Metrics:rmse:{rmse},mae:{mae},r2:{r2}\")       \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8def34f2",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:25.236094Z",
     "iopub.status.busy": "2023-08-20T11:07:25.235296Z",
     "iopub.status.idle": "2023-08-20T11:07:25.239839Z",
     "shell.execute_reply": "2023-08-20T11:07:25.238980Z"
    },
    "papermill": {
     "duration": 0.040752,
     "end_time": "2023-08-20T11:07:25.242087",
     "exception": false,
     "start_time": "2023-08-20T11:07:25.201335",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "from sklearn.metrics import ConfusionMatrixDisplay,confusion_matrix"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b28b789e",
   "metadata": {
    "execution": {
     "iopub.execute_input": "2023-08-20T11:07:25.304110Z",
     "iopub.status.busy": "2023-08-20T11:07:25.303358Z",
     "iopub.status.idle": "2023-08-20T11:07:25.844505Z",
     "shell.execute_reply": "2023-08-20T11:07:25.843415Z"
    },
    "papermill": {
     "duration": 0.575292,
     "end_time": "2023-08-20T11:07:25.847088",
     "exception": false,
     "start_time": "2023-08-20T11:07:25.271796",
     "status": "completed"
    },
    "tags": []
   },
   "outputs": [],
   "source": [
    "cmd=ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test,y_pred,labels=lr.classes_),display_labels=lr.classes_)\n",
    "cmd.plot()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "148005a9",
   "metadata": {},
   "outputs": [],
   "source": [
    "# close mlflow connection\n",
    "run_id = run.info.run_uuid\n",
    "experiment_id = run.info.experiment_id\n",
    "mlflow.end_run()\n",
    "print(mlflow.get_artifact_uri())\n",
    "#print(f'artifact_uri = {mlflow.get_artifact_uri()}')\n",
    "print(\"runID: %s\" % run_id)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "1a694c18",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.3"
  },
  "papermill": {
   "default_parameters": {},
   "duration": 47.968457,
   "end_time": "2023-08-20T11:07:52.713371",
   "environment_variables": {},
   "exception": null,
   "input_path": "__notebook__.ipynb",
   "output_path": "__notebook__.ipynb",
   "parameters": {},
   "start_time": "2023-08-20T11:07:04.744914",
   "version": "2.4.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
