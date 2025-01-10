/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import { API } from 'aws-amplify';

const SERVER_API = {

    async getList() {
        const apiName = 'ci-api';
        const path = '/list';
        return await API.post(apiName, path);
    },

    async getDetails(key) {
        const apiName = 'ci-api';
        const path = `/details/${key}`;
        return await API.post(apiName, path);
    },
};

export default SERVER_API;