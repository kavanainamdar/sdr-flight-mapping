CREATE TABLE [dbo].[AdsbAircraftData](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[BatchTimeUtc] [datetime2](7) NULL,
	[Hex] [nvarchar](10) NULL,
	[Flight] [nvarchar](20) NULL,
	[Lat] [float] NULL,
	[Lon] [float] NULL,
	[Altitude] [int] NULL,
	[GroundSpeed] [float] NULL,
	[Track] [float] NULL,
	[Seen] [float] NULL,
	[AircraftJson] [nvarchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]