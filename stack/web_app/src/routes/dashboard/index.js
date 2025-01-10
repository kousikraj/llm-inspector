/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import React, { useState, useEffect, useRef } from "react";
import { useParams } from "react-router";
import { AuditMetaView } from './audit-meta';
import { ContentLayout, Header, Grid, Container, SpaceBetween, Flashbar, Spinner, Button, Link } from '@cloudscape-design/components';

import Layout from '../../layout';
import { SERVER_API, Util } from '../../common';
import DataGenerator from "./dataGenerator";
import {ImageAndAnalysis} from "./image-analysis";
import {AuditDetail} from "./audit-detail";

const breadItems = [
    { text: "Home", href: "../../" },
    { text: "Requests", href: "../../" },
    { text: "Details", href: "#" },
]

const Dashboard = ({ userid }) => {

    const { authStatus, utilities, GenerateBreadcrumb } = Util();
    const { key } = useParams();
    const [loading, setLoading] = useState(true);
    const [requestDetails, setRequestDetails] = useState(null);
    const [imageData, setImageData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        if (authStatus === "authenticated") {
            const init = async () => {
                let apiData = await SERVER_API.getDetails(key);
                setRequestDetails(apiData["item"]);
                setImageData(apiData["presignedUrl"]);
                setIsLoading(false);
            }
            init()
        }
    }, [authStatus, key, userid]);

    return (
        <Layout
            id="main_panel"
            navUtilities={utilities()}
            breadcrumb={GenerateBreadcrumb(breadItems)}
        >
            <ContentLayout
                header={
                    <Header variant="h1" actions={<></>}>
                        Request Details
                    </Header>
                }>
                {isLoading ?
                    <Container header={<Header variant="h2">Loading...</Header>}>
                        <Spinner size="large" ></Spinner>
                    </Container>
                    :
                    <SpaceBetween size="l">
                        <AuditMetaView item={requestDetails} isLoading={isLoading}/>
                        <ImageAndAnalysis item={requestDetails} image={imageData} isLoading={isLoading}/>
                        <AuditDetail item={requestDetails} isLoading={isLoading}/>
                    </SpaceBetween>
                }
            </ContentLayout>
        </Layout>
    );
};


export default Dashboard;