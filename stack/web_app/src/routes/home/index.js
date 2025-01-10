/*
 * # Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * # SPDX-License-Identifier: MIT-0
 */

import React, { useEffect, useState } from 'react'
import { Grid, ContentLayout, Link, Header } from "@cloudscape-design/components";

import Layout from '../../layout';
import { SERVER_API, Util } from '../../common';
import { AuditTable } from '../../components/AuditTable';

const processData = (data) => {
    let processData = [];
    data.forEach(element => {
        processData.push(element);
    });
    processData = processData.sort((a, b) => {
        return Date.parse(b.iTD) - Date.parse(a.iTD);
    });
    return processData;
}
const Home = () => {
    const { authStatus, utilities, GenerateBreadcrumb } = Util();

    const [loading, setLoading] = useState(true);
    const [llmAuditList, setLLMAuditList] = useState([]);

    const breadItems = [
        { text: "Home", href: "../" },
        { text: "Requests", href: "#" },
    ]

    useEffect(() => {
        if (authStatus === "authenticated") {
            const init = async () => {
                let apiListData = await SERVER_API.getList();
                setLLMAuditList(processData(apiListData));
                setLoading(false);
            }
            init();
        }
    }, [authStatus])

    return (<>
        <Layout
            id="main_panel"
            navUtilities={utilities()}
            breadcrumb={GenerateBreadcrumb(breadItems)}
        >
            <ContentLayout
                header={
                    <Header
                        variant="h1"
                        description="Select an audit record to view details."
                        info={<Link variant="info" ariaLabel="Info goes here.">Info</Link>}>
                        Requests
                    </Header>
                }>
                <Grid
                    gridDefinition={[
                        { colspan: { default: 12 } },
                        { colspan: { default: 12 } }
                    ]}>
                    <AuditTable data={llmAuditList} loading={loading} />
                </Grid>
            </ContentLayout>
        </Layout>
    </>);
};

export default Home;