from geometry import *

class Feature:
    def __init__(self, ContainmentDateTime,ControlDateTime,IncidentSize,DiscoveryAcres,FinalAcres, FireCause,FireCauseSpecific,FireDiscoveryDateTime, FireOutDateTime, FireStrategyPointZonePercent, IncidentName, IncidentShortDescription, IncidentTypeKind, IsFireCauseInvestigated, IsFireCodeRequested, CreatedOnDateTime_dt, ModifiedOnDateTime_dt, SourceGlobalID, IncidentComplexityLevel, POOCity, POOCounty, SourceOID, FireStrategyMonitorPercent, InitialLatitude, InitialLongitude, geometry):
        
        self.SourceOID = SourceOID
        self.ContainmentDateTime = ContainmentDateTime
        self.ControlDateTime = ControlDateTime
        self.IncidentSize = IncidentSize
        self.DiscoveryAcres = DiscoveryAcres
        self.FinalAcres = FinalAcres
        self.FireCause = FireCause
        self.FireCauseSpecific = FireCauseSpecific
        self.FireDiscoveryDateTime = FireDiscoveryDateTime
        self.FireOutDateTime = FireOutDateTime
        self.FireStrategyPointZonePercent = FireStrategyPointZonePercent
        self.IncidentName = IncidentName
        self.IncidentShortDescription = IncidentShortDescription
        self.IncidentTypeKind = IncidentTypeKind
        self.IsFireCauseInvestigated = IsFireCauseInvestigated
        self.IsFireCodeRequested = IsFireCodeRequested
        self.CreatedOnDateTime_dt = CreatedOnDateTime_dt
        self.ModifiedOnDateTime_dt = ModifiedOnDateTime_dt
        self.SourceGlobalID = SourceGlobalID
        self.IncidentComplexityLevel = IncidentComplexityLevel
        self.FireStrategyMonitorPercent = FireStrategyMonitorPercent
        self.InitialLatitude = InitialLatitude
        self.InitialLongitude = InitialLongitude
        self.POOCity = POOCity
        self.POOCounty = POOCounty
        self.geometry = Geometry(**geometry)