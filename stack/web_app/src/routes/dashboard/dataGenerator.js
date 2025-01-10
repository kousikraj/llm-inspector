/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import { Formatter } from "../../format";
import { Sentiment } from "../../components/Sentiment";

const sentimentValue = (txt) => {
    let val = 0;
    switch (txt) {
        case 'POSITIVE': val = 2; break;
        case 'NEGATIVE': val = -2; break;
        default: val = 0;
    }
    return val;
}

const getSentimentScore = (txt, obj) => {
    let val = 0;
    switch (txt) {
        case 'POSITIVE': val = obj.Positive; break;
        case 'NEGATIVE': val = -1 * obj.Negative; break;
        default: val = 0;
    }
    return val;
}

class DataGenerator {
    details = null;
    media = {
        url:""
    }

    constructor(data) {
        this.details = data;
        this.processData();
    }

    processData() {
    }
}

export default DataGenerator;