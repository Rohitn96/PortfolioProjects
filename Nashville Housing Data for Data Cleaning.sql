-- Data Cleaning Project 

-- Nashville Housing Data

-- To view the data

Select * 
From PortfolioProject..NashvilleHousing


-- To standardize the date format


Alter Table NashvilleHousing
Add SaleDateConverted Date

Update NashvilleHousing
Set SaleDateConverted = Convert(Date, SaleDate)

Select SaleDateConverted
From PortfolioProject..NashvilleHousing


-- Populate Property Address Data


Select *
From PortfolioProject..NashvilleHousing
--Where PropertyAddress is null
order by ParcelID

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject..NashvilleHousing a
Join PortfolioProject..NashvilleHousing b
	on a.ParcelID = b.ParcelID
	And a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

Update a
Set PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject..NashvilleHousing a
Join PortfolioProject..NashvilleHousing b
	on a.ParcelID = b.ParcelID
	And a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null


-- Breaking the address into diffrent columns


Select PropertyAddress
From PortfolioProject..NashvilleHousing

Select
Substring(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1) as Address
, Substring(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress))  as Address
From PortfolioProject..NashvilleHousing

Alter Table NashvilleHousing
ADD PropertyAddressSplit Varchar(255)

Update NashvilleHousing
Set PropertyAddressSplit = Substring(PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1)

Alter Table NashvilleHousing
Add PropertyCitySplit Varchar(255)

Update NashvilleHousing
Set PropertyCitySplit = Substring(PropertyAddress, CHARINDEX(',', PropertyAddress)+1, LEN(PropertyAddress))


Select OwnerAddress
From PortfolioProject..NashvilleHousing

Select
PARSENAME(Replace(OwnerAddress, ',','.'),3)
,PARSENAME(Replace(OwnerAddress, ',','.'),2)
,PARSENAME(Replace(OwnerAddress, ',','.'),1)
From PortfolioProject..NashvilleHousing

Alter Table NashvilleHousing
Add OwnerAddressSplit Varchar(255)

Update NashvilleHousing
Set OwnerAddressSplit = PARSENAME(Replace(OwnerAddress, ',','.'),3)

Alter Table NashvilleHousing
Add OwnerCitySplit Varchar(255)

Update NashvilleHousing
Set OwnerCitySplit = PARSENAME(Replace(OwnerAddress, ',','.'),2)

Alter Table NashvilleHousing
Add OwnerStateSplit Varchar(255)

Update NashvilleHousing
Set OwnerStateSplit = PARSENAME(Replace(OwnerAddress, ',','.'),1)

Select *
From PortfolioProject..NashvilleHousing


-- Standardizing the values in SoldAsVacant column


Select Distinct(SoldAsVacant), Count(SoldAsVacant)
From PortfolioProject..NashvilleHousing
Group by SoldAsVacant

Select SoldAsVacant,
Case when SoldAsVacant = 'Y' Then 'Yes'
	 when SoldAsVacant = 'N' Then 'No'
	 Else SoldAsVacant
	 End
From PortfolioProject..NashvilleHousing

Update NashvilleHousing
Set SoldAsVacant = Case when SoldAsVacant = 'Y' Then 'Yes'
	 when SoldAsVacant = 'N' Then 'No'
	 Else SoldAsVacant
	 End


-- Remove Duplicates


WITH RowNumCTE AS(
Select *,
	ROW_NUMBER() OVER (
	PARTITION BY ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 ORDER BY
					UniqueID
					) row_num
From PortfolioProject..NashvilleHousing
)
Delete *
From RowNumCTE
Where row_num > 1
Order by PropertyAddress


Select * 
From PortfolioProject..NashvilleHousing


-- Delete unused columns


Select * 
From PortfolioProject..NashvilleHousing

Alter Table PortfolioProject..NashvilleHousing
Drop Column PropertyAddress, SaleDate, OwnerAddress


