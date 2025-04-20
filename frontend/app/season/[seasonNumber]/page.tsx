import React from "react";
import { Card } from "@/app/components";
import { BarChart } from "@/app/components";
import TopMatter from "@/app/components/topmatter/topmatter";
import {
    Region,
    Role,
    Slot,
    get_disclaimer,
    get_occurrences,
    get_season_list,
    map_generic_kv_to_bar_chart_data,
    calculateGiniCoefficient,
    load,
} from "@/app/server/actions";
import { Tabs, TabsList, TabsTab, TabsPanel } from "@mantine/core";

export async function generateStaticParams() {
    return (await get_season_list()).map((season) => ({
        seasonNumber: season.toString(),
    }));
}

const SeasonPage = async ({ params }: { params: { seasonNumber: number } }) => {
    const regions = [Region.AMERICAS, Region.EUROPE, Region.ASIA];
    const roles = [Role.SUPPORT, Role.DAMAGE, Role.TANK];
    const hasOpenQueue =
        load(params.seasonNumber).entries.filter((e) => e.openqueue).length !==
        0;

    return (
        <main>
            <TopMatter
                seasonNumber={params.seasonNumber.toString()}
                disclaimer={await get_disclaimer(params.seasonNumber)}
            />
            <Tabs
                defaultValue="RoleQueue"
                color="cyan"
                variant="pills"
                radius="xs"
            >
                <TabsList>
                    <TabsTab value="RoleQueue">Role Queue</TabsTab>
                    <TabsTab value="OpenQueue" disabled={!hasOpenQueue}>
                        Open Queue
                    </TabsTab>
                </TabsList>
                <TabsPanel value="RoleQueue">
                    <Card title="Hero Occurrences: All Slots" nowrap>
                        <p className="">
                            The data is calculated by applying weights to the
                            second most played and third most played slots. This
                            provides a more accurate analysis of popular picks
                            by estimating the playtime ratio to the first most
                            played. These weights can be found{" "}
                            <a
                                className="text-blue-500 underline"
                                href="https://github.com/thearyadev/top500-aggregator/blob/a20fb6b1b8e5beac6e5c35f88cc5de863121ce93/frontend/app/server/actions.ts#L145"
                            >
                                here
                            </a>
                        </p>
                        <Tabs defaultValue="Raw">
                            <TabsList>
                                <TabsTab value="Weighted">Weighted</TabsTab>
                                <TabsTab value="Raw">Raw</TabsTab>
                            </TabsList>
                            <TabsPanel value="Weighted">
                                <div className="pt-10" />
                                <BarChart
                                    title="Americas"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.AMERICAS,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.AMERICAS,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="Europe"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.EUROPE,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.EUROPE,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="Asia"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.ASIA,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.ASIA,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="All Regions"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            null,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                null,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={1200}
                                />
                            </TabsPanel>

                            <TabsPanel value="Raw">
                                <div className="pt-10" />
                                <BarChart
                                    title="Americas"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.AMERICAS,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.AMERICAS,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="Europe"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.EUROPE,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.EUROPE,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="Asia"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.ASIA,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.ASIA,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={500}
                                />
                                <BarChart
                                    title="All Regions"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            null,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                null,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={1200}
                                />
                            </TabsPanel>
                        </Tabs>
                    </Card>
                    <Card title="Hero Occurrences: First Most Played">
                        {roles.map((role) => {
                            return regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${role}: ${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                role,
                                                region,
                                                Slot.firstMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    role,
                                                    region,
                                                    Slot.firstMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    false,
                                                ),
                                            ),
                                        )}
                                        maxY={400}
                                    />
                                );
                            });
                        })}
                        {roles.map(async (role) => {
                            return (
                                <BarChart
                                    title={`${role}: All`}
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            role,
                                            null,
                                            Slot.firstMostPlayed,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                role,
                                                null,
                                                Slot.firstMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={700}
                                />
                            );
                        })}
                    </Card>
                    <Card title="Hero Occurrences: Second Most Played">
                        {roles.map((role) => {
                            return regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${role}: ${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                role,
                                                region,
                                                Slot.secondMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    role,
                                                    region,
                                                    Slot.secondMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    false,
                                                ),
                                            ),
                                        )}
                                        maxY={400}
                                    />
                                );
                            });
                        })}
                        {roles.map(async (role) => {
                            return (
                                <BarChart
                                    title={`${role}: All`}
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            role,
                                            null,
                                            Slot.secondMostPlayed,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                role,
                                                null,
                                                Slot.secondMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={650}
                                />
                            );
                        })}
                    </Card>
                    <Card title="Hero Occurrences: Third Most Played">
                        {roles.map((role) => {
                            return regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${role}: ${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                role,
                                                region,
                                                Slot.thirdMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    role,
                                                    region,
                                                    Slot.thirdMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    false,
                                                ),
                                            ),
                                        )}
                                        maxY={400}
                                    />
                                );
                            });
                        })}
                        {roles.map(async (role) => {
                            return (
                                <BarChart
                                    title={`${role}: All`}
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            role,
                                            null,
                                            Slot.thirdMostPlayed,
                                            params.seasonNumber,
                                            false,
                                            false,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                role,
                                                null,
                                                Slot.thirdMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                false,
                                            ),
                                        ),
                                    )}
                                    maxY={700}
                                />
                            );
                        })}
                    </Card>
                </TabsPanel>
                <TabsPanel value="OpenQueue">
                    <Card title="Hero Occurrences: All Slots" nowrap>
                        <p className="">
                            The data is calculated by applying weights to the
                            second most played and third most played slots. This
                            provides a more accurate analysis of popular picks
                            by estimating the playtime ratio to the first most
                            played. These weights can be found{" "}
                            <a
                                className="text-blue-500 underline"
                                href="https://github.com/thearyadev/top500-aggregator/blob/a20fb6b1b8e5beac6e5c35f88cc5de863121ce93/frontend/app/server/actions.ts#L145"
                            >
                                here
                            </a>
                        </p>
                        <Tabs defaultValue="Raw">
                            <TabsList>
                                <TabsTab value="Weighted">Weighted</TabsTab>
                                <TabsTab value="Raw">Raw</TabsTab>
                            </TabsList>
                            <TabsPanel value="Weighted">
                                <div className="pt-10" />
                                <BarChart
                                    title="Americas"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.AMERICAS,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.AMERICAS,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="Europe"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.EUROPE,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.EUROPE,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="Asia"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.ASIA,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.ASIA,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="All Regions"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            null,
                                            null,
                                            params.seasonNumber,
                                            true,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                null,
                                                null,
                                                params.seasonNumber,
                                                true,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={1200}
                                />
                            </TabsPanel>

                            <TabsPanel value="Raw">
                                <div className="pt-10" />
                                <BarChart
                                    title="Americas"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.AMERICAS,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.AMERICAS,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="Europe"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.EUROPE,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.EUROPE,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="Asia"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            Region.ASIA,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                Region.ASIA,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={300}
                                />
                                <BarChart
                                    title="All Regions"
                                    graph={map_generic_kv_to_bar_chart_data(
                                        await get_occurrences(
                                            null,
                                            null,
                                            null,
                                            params.seasonNumber,
                                            false,
                                            true,
                                        ),
                                    )}
                                    giniCoefficient={calculateGiniCoefficient(
                                        Object.values(
                                            await get_occurrences(
                                                null,
                                                null,
                                                null,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        ),
                                    )}
                                    maxY={1200}
                                />
                            </TabsPanel>
                        </Tabs>
                    </Card>

                    <Card title="Hero Occurrences: First Most Played">
                        <div className="col-span-3">
                            {regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                null,
                                                region,
                                                Slot.firstMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    null,
                                                    region,
                                                    Slot.firstMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    true,
                                                ),
                                            ),
                                        )}
                                        maxY={150}
                                    />
                                );
                            })}
                        </div>
                    </Card>
                    <Card title="Hero Occurrences: Second Most Played">
                        <div className="col-span-3">
                            {regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                null,
                                                region,
                                                Slot.firstMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    null,
                                                    region,
                                                    Slot.secondMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    true,
                                                ),
                                            ),
                                        )}
                                        maxY={150}
                                    />
                                );
                            })}
                        </div>
                    </Card>
                    <Card title="Hero Occurrences: Third Most Played">
                        <div className="col-span-3">
                            {regions.map(async (region) => {
                                return (
                                    <BarChart
                                        title={`${region}`}
                                        graph={map_generic_kv_to_bar_chart_data(
                                            await get_occurrences(
                                                null,
                                                region,
                                                Slot.firstMostPlayed,
                                                params.seasonNumber,
                                                false,
                                                true,
                                            ),
                                        )}
                                        giniCoefficient={calculateGiniCoefficient(
                                            Object.values(
                                                await get_occurrences(
                                                    null,
                                                    region,
                                                    Slot.thirdMostPlayed,
                                                    params.seasonNumber,
                                                    false,
                                                    true,
                                                ),
                                            ),
                                        )}
                                        maxY={150}
                                    />
                                );
                            })}
                        </div>
                    </Card>
                </TabsPanel>
            </Tabs>
        </main>
    );
};

export default SeasonPage;
