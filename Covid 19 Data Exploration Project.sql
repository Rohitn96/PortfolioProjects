
-- Covid 19 Worldwide Data Exploration

-- Skills used: Joins, CTE's, Temp Tables, Windows Functions, Aggregate Functions, Creating Views, Converting Data Types

-- Overview of the data
-- This table has data related to deaths
Select * 
From PortfolioProject..CovidDeaths
Order by 3,4

-- This table has data related to vaccinations
Select * 
From PortfolioProject..CovidVaccinations
Order by 3,4

-- Selecting the data that we could use

Select location, date, total_cases, new_cases, total_deaths, population
From PortfolioProject..CovidDeaths
order by 1,2


-- To check the Total Cases vs Total Deaths

Select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
order by 1,2

-- To check the location specific Death Percentage

Select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
Where location like '%Finland%'
order by 1,2

-- To check the total population infected by covid

Select location, date, population,total_cases,  (total_cases/population)*100 as InfectedPopulationPercentage
From PortfolioProject..CovidDeaths
Where location like '%Finland%'
order by 1,2

-- To check the countries with highest infection rate.

Select location,population, max(total_cases) as HighestInfectionCount, max((total_cases/population))*100 as InfectedPopulationPercentage
From PortfolioProject..CovidDeaths
Group by location, population
order by InfectedPopulationPercentage desc

-- To check the countries with highest deaths.

Select location,population, max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
where continent is not null
Group by location, population
order by TotalDeathCount desc

-- To check the continents with highest death

Select continent, max(cast(total_deaths as int)) as TotalDeathCount
From PortfolioProject..CovidDeaths
where continent is not null
Group by continent
order by TotalDeathCount desc

-- To check the data across the world

Select Date, sum(new_cases) as TotalCases, sum(cast(new_deaths as int)) as TotalDeaths, sum(cast(new_deaths as int))/sum(new_cases)*100 as DeathPercentage
From PortfolioProject..CovidDeaths
where continent is not null
group by date
order by 1,2

-- Merging both data about death with data about vaccination

Select *
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location 
	and dea.date = vac.date
order by 2,3

-- Looking at Total Population vs Vaccinations

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations 
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location 
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- To check the progress of people being vaccinated

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location order by dea.location, dea.date) as VaccinatedPopulation
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location 
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

-- Using CTE's to perfrom calulations on the previous query

with PopvsVac (continent, location, date, population, new_vaccinations, VaccinatedPopulation) 
as 
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations, 
sum(cast(vac.new_vaccinations as int)) over (partition by dea.location Order by dea.location, dea.date) as VaccinatedPopulation
From PortfolioProject..CovidDeaths dea
Join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location 
	and dea.date = vac.date
where dea.continent is not null
)
Select *, (VaccinatedPopulation/population)*100
From PopvsVac

-- Creating Temp Table

IF OBJECT_ID('tempdb..#VaccinatedPopulationPercentage') IS NOT NULL
    DROP TABLE #VaccinatedPopulationPercentage;
CREATE TABLE #VaccinatedPopulationPercentage
(
    Continent nvarchar(255),
    Location varchar(255),
    Date datetime,
    Population numeric,
    New_vaccinations numeric,
    VaccinatedPopulation bigint
);
INSERT INTO #VaccinatedPopulationPercentage
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS bigint)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS VaccinatedPopulation
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
    ON dea.location = vac.location
    AND dea.date = vac.date;

SELECT *,
       CASE
           WHEN Population = 0 THEN NULL
           ELSE (VaccinatedPopulation / Population) * 100
       END AS VaccinationPercentage
FROM #VaccinatedPopulationPercentage;

-- Creating view to strore data for later visualizations

Create view VaccinatedPopulationPercentage as
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CAST(vac.new_vaccinations AS bigint)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS VaccinatedPopulation
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
    ON dea.location = vac.location
    AND dea.date = vac.date
where dea.continent is not null

Select * From VaccinatedPopulationPercentage

