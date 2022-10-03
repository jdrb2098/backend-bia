from email.policy import default
from random import choices
from tkinter.tix import Tree
from turtle import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
paises_CHOICES = (
    ('AF', 'AFGHANISTAN'),
    ('AL', 'ALBANIA'),
    ('DZ', 'ALGERIA'),
    ('AS', 'AMERICAN SAMOA'),
    ('AD', 'ANDORRA'),
    ('AO', 'ANGOLA'),
    ('AI', 'ANGUILLA'),
    ('AQ', 'ANTARCTICA'),
    ('AG', 'ANTIGUA AND BARBUDA'),
    ('AR', 'ARGENTINA'),
    ('AM', 'ARMENIA'),
    ('AW', 'ARUBA'),
    ('AU', 'AUSTRALIA'),
    ('AT', 'AUSTRIA'),
    ('AZ', 'AZERBAIJAN'),
    ('BS', 'BAHAMAS'),
    ('BH', 'BAHRAIN'),
    ('BD', 'BANGLADESH'),
    ('BB', 'BARBADOS'),
    ('BY', 'BELARUS'),
    ('BE', 'BELGIUM'),
    ('BZ', 'BELIZE'),
    ('BJ', 'BENIN'),
    ('BM', 'BERMUDA'),
    ('BT', 'BHUTAN'),
    ('BO', 'BOLIVIA'),
    ('BA', 'BOSNIA AND HERZEGOVINA'),
    ('BW', 'BOTSWANA'),
    ('BV', 'BOUVET ISLAND'),
    ('BR', 'BRAZIL'),
    ('IO', 'BRITISH INDIAN OCEAN TERRITORY'),
    ('BN', 'BRUNEI DARUSSALAM'),
    ('BG', 'BULGARIA'),
    ('BF', 'BURKINA FASO'),
    ('BI', 'BURUNDI'),
    ('KH', 'CAMBODIA'),
    ('CM', 'CAMEROON'),
    ('CA', 'CANADA'),
    ('CV', 'CAPE VERDE'),
    ('KY', 'CAYMAN ISLANDS'),
    ('CF', 'CENTRAL AFRICAN REPUBLIC'),
    ('TD', 'CHAD'),
    ('CL', 'CHILE'),
    ('CN', 'CHINA'),
    ('CX', 'CHRISTMAS ISLAND'),
    ('CC', 'COCOS (KEELING) ISLANDS'),
    ('CO', 'COLOMBIA'),
    ('KM', 'COMOROS'),
    ('CG', 'CONGO'),
    ('CD', 'CONGO, THE DEMOCRATIC REPUBLIC OF'),
    ('CK', 'COOK ISLANDS'),
    ('CR', 'COSTA RICA'),
    ('CI', "CÃ”TE D'IVOIRE"),
    ('HR', 'CROATIA'),
    ('CU', 'CUBA'),
    ('CY', 'CYPRUS'),
    ('CZ', 'CZECH REPUBLIC'),
    ('DK', 'DENMARK'),
    ('DJ', 'DJIBOUTI'),
    ('DM', 'DOMINICA'),
    ('DO', 'DOMINICAN REPUBLIC'),
    ('EC', 'ECUADOR'),
    ('EG', 'EGYPT'),
    ('SV', 'EL SALVADOR'),
    ('GQ', 'EQUATORIAL GUINEA'),
    ('ER', 'ERITREA'),
    ('EE', 'ESTONIA'),
    ('ET', 'ETHIOPIA'),
    ('FK', 'FALKLAND ISLANDS (MALVINAS)'),
    ('FO', 'FAROE ISLANDS'),
    ('FJ', 'FIJI'),
    ('FI', 'FINLAND'),
    ('FR', 'FRANCE'),
    ('GF', 'FRENCH GUIANA'),
    ('PF', 'FRENCH POLYNESIA'),
    ('TF', 'FRENCH SOUTHERN TERRITORIES'),
    ('GA', 'GABON'),
    ('GM', 'GAMBIA'),
    ('GE', 'GEORGIA'),
    ('DE', 'GERMANY'),
    ('GH', 'GHANA'),
    ('GI', 'GIBRALTAR'),
    ('GR', 'GREECE'),
    ('GL', 'GREENLAND'),
    ('GD', 'GRENADA'),
    ('GP', 'GUADELOUPE'),
    ('GU', 'GUAM'),
    ('GT', 'GUATEMALA'),
    ('GN', 'GUINEA'),
    ('GW', 'GUINEA'),
    ('GY', 'GUYANA'),
    ('HT', 'HAITI'),
    ('HM', 'HEARD ISLAND AND MCDONALD ISLANDS'),
    ('HN', 'HONDURAS'),
    ('HK', 'HONG KONG'),
    ('HU', 'HUNGARY'),
    ('IS', 'ICELAND'),
    ('IN', 'INDIA'),
    ('ID', 'INDONESIA'),
    ('IR', 'IRAN, ISLAMIC REPUBLIC OF'),
    ('IQ', 'IRAQ'),
    ('IE', 'IRELAND'),
    ('IL', 'ISRAEL'),
    ('IT', 'ITALY'),
    ('JM', 'JAMAICA'),
    ('JP', 'JAPAN'),
    ('JO', 'JORDAN'),
    ('KZ', 'KAZAKHSTAN'),
    ('KE', 'KENYA'),
    ('KI', 'KIRIBATI'),
    ('KP', "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF"),
    ('KR', 'KOREA, REPUBLIC OF'),
    ('KW', 'KUWAIT'),
    ('KG', 'KYRGYZSTAN'),
    ('LA', "LAO PEOPLE'S DEMOCRATIC REPUBLIC"),
    ('LV', 'LATVIA'),
    ('LB', 'LEBANON'),
    ('LS', 'LESOTHO'),
    ('LR', 'LIBERIA'),
    ('LY', 'LIBYAN ARAB JAMAHIRIYA'),
    ('LI', 'LIECHTENSTEIN'),
    ('LT', 'LITHUANIA'),
    ('LU', 'LUXEMBOURG'),
    ('MO', 'MACAO'),
    ('MK', 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF'),
    ('MG', 'MADAGASCAR'),
    ('MW', 'MALAWI'),
    ('MY', 'MALAYSIA'),
    ('MV', 'MALDIVES'),
    ('ML', 'MALI'),
    ('MT', 'MALTA'),
    ('MH', 'MARSHALL ISLANDS'),
    ('MQ', 'MARTINIQUE'),
    ('MR', 'MAURITANIA'),
    ('MU', 'MAURITIUS'),
    ('YT', 'MAYOTTE'),
    ('MX', 'MEXICO'),
    ('FM', 'MICRONESIA, FEDERATED STATES OF'),
    ('MD', 'MOLDOVA, REPUBLIC OF'),
    ('MC', 'MONACO'),
    ('MN', 'MONGOLIA'),
    ('MS', 'MONTSERRAT'),
    ('MA', 'MOROCCO'),
    ('MZ', 'MOZAMBIQUE'),
    ('MM', 'MYANMAR'),
    ('NA', 'NAMIBIA'),
    ('NR', 'NAURU'),
    ('NP', 'NEPAL'),
    ('NL', 'NETHERLANDS'),
    ('AN', 'NETHERLANDS ANTILLES'),
    ('NC', 'NEW CALEDONIA'),
    ('NZ', 'NEW ZEALAND'),
    ('NI', 'NICARAGUA'),
    ('NE', 'NIGER'),
    ('NG', 'NIGERIA'),
    ('NU', 'NIUE'),
    ('NF', 'NORFOLK ISLAND'),
    ('MP', 'NORTHERN MARIANA ISLANDS'),
    ('NO', 'NORWAY'),
    ('OM', 'OMAN'),
    ('PK', 'PAKISTAN'),
    ('PW', 'PALAU'),
    ('PS', 'PALESTINIAN TERRITORY, OCCUPIED'),
    ('PA', 'PANAMA'),
    ('PG', 'PAPUA NEW GUINEA'),
    ('PY', 'PARAGUAY'),
    ('PE', 'PERU'),
    ('PH', 'PHILIPPINES'),
    ('PN', 'PITCAIRN'),
    ('PL', 'POLAND'),
    ('PT', 'PORTUGAL'),
    ('PR', 'PUERTO RICO'),
    ('QA', 'QATAR'),
    ('RE', 'RÃ‰UNION'),
    ('RO', 'ROMANIA'),
    ('RU', 'RUSSIAN FEDERATION'),
    ('RW', 'RWANDA'),
    ('SH', 'SAINT HELENA'),
    ('KN', 'SAINT KITTS AND NEVIS'),
    ('LC', 'SAINT LUCIA'),
    ('PM', 'SAINT PIERRE AND MIQUELON'),
    ('VC', 'SAINT VINCENT AND THE GRENADINES'),
    ('WS', 'SAMOA'),
    ('SM', 'SAN MARINO'),
    ('ST', 'SAO TOME AND PRINCIPE'),
    ('SA', 'SAUDI ARABIA'),
    ('SN', 'SENEGAL'),
    ('CS', 'SERBIA AND MONTENEGRO'),
    ('SC', 'SEYCHELLES'),
    ('SL', 'SIERRA LEONE'),
    ('SG', 'SINGAPORE'),
    ('SK', 'SLOVAKIA'),
    ('SI', 'SLOVENIA'),
    ('SB', 'SOLOMON ISLANDS'),
    ('SO', 'SOMALIA'),
    ('ZA', 'SOUTH AFRICA'),
    ('GS', 'SOUTH GEORGIA AND SOUTH SANDWICH ISLANDS'),
    ('ES', 'SPAIN'),
    ('LK', 'SRI LANKA'),
    ('SD', 'SUDAN'),
    ('SR', 'SURINAME'),
    ('SJ', 'SVALBARD AND JAN MAYEN'),
    ('SZ', 'SWAZILAND'),
    ('SE', 'SWEDEN'),
    ('CH', 'SWITZERLAND'),
    ('SY', 'SYRIAN ARAB REPUBLIC'),
    ('TW', 'TAIWAN, PROVINCE OF CHINA'),
    ('TJ', 'TAJIKISTAN'),
    ('TZ', 'TANZANIA, UNITED REPUBLIC OF'),
    ('TH', 'THAILAND'),
    ('TL', 'TIMOR'),
    ('TG', 'TOGO'),
    ('TK', 'TOKELAU'),
    ('TO', 'TONGA'),
    ('TT', 'TRINIDAD AND TOBAGO'),
    ('TN', 'TUNISIA'),
    ('TR', 'TURKEY'),
    ('TM', 'TURKMENISTAN'),
    ('TC', 'TURKS AND CAICOS ISLANDS'),
    ('TV', 'TUVALU'),
    ('UG', 'UGANDA'),
    ('UA', 'UKRAINE'),
    ('AE', 'UNITED ARAB EMIRATES'),
    ('GB', 'UNITED KINGDOM'),
    ('US', 'UNITED STATES'),
    ('UM', 'UNITED STATES MINOR OUTLYING ISLANDS'),
    ('UY', 'URUGUAY'),
    ('UZ', 'UZBEKISTAN'),
    ('VU', 'VANUATU'),
    ('VN', 'VIET NAM'),
    ('VG', 'VIRGIN ISLANDS, BRITISH'),
    ('VI', 'VIRGIN ISLANDS, U.S.'),
    ('WF', 'WALLIS AND FUTUNA'),
    ('EH', 'WESTERN SAHARA'),
    ('YE', 'YEMEN'),
    ('ZW', 'ZIMBABWE')
)
departamentos_CHOICES = (
    ('05', 'ANTIOQUIA'),
    ('08', 'ATLANTICO'),
    ('11', 'BOGOTA'),
    ('13', 'BOLIVAR'),
    ('15', 'BOYACA'),
    ('17', 'CALDAS'),
    ('18', 'CAQUETA'),
    ('19', 'CAUCA'),
    ('20', 'CESAR'),
    ('23', 'CORDOBA'),
    ('25', 'CUNDINAMARCA'),
    ('27', 'CHOCO'),
    ('41', 'HUILA'),
    ('44', 'LA GUAJIRA'),
    ('47', 'MAGDALENA'),
    ('50', 'META'),
    ('52', 'NARIÑO'),
    ('54', 'N. DE SANTANDER'),
    ('63', 'QUINDIO'),
    ('66', 'RISARALDA'),
    ('68', 'SANTANDER'),
    ('70', 'SUCRE'),
    ('73', 'TOLIMA'),
    ('76', 'VALLE DEL CAUCA'),
    ('81', 'ARAUCA'),
    ('85', 'CASANARE'),
    ('86', 'PUTUMAYO'),
    ('88', 'SAN ANDRES'),
    ('91', 'AMAZONAS'),
    ('94', 'GUANIA'),
    ('95', 'GUAVIARE'),
    ('97', 'VAUPES'),
    ('99', 'VICHADA')
)
municipios_CHOICES = (
    #AMAZONAS
('91263', 'El Encanto'),
('91405', 'La Chorrera'),
('91407', 'La Pedrera'),
('91430', 'La Victoria'),
('91001', 'Leticia'),
('91460', 'Miriti - Paraná'),
('91530', 'Puerto Alegria'),
('91536', 'Puerto Arica'),
('91540', 'Puerto Nariño'),
('91669', 'Puerto Santander'),
('91798', 'Tarapacá'),
#ANTIOQUIA
('05120', 'Cáceres'),
('05154', 'Caucasia'),
('05250', 'El Bagre'),
('05495', 'Nechí'),
('05790', 'Tarazá'),
('05895', 'Zaragoza'),
('05142', 'Caracolí'),
('05425', 'Maceo'),
('05579', 'Puerto Berrio'),
('05585', 'Puerto Nare'),
('05591', 'Puerto Triunfo'),
('05893', 'Yondó'),
('05031', 'Amalfi'),
('05040', 'Anorí'),
('05190', 'Cisneros'),
('05604', 'Remedios'),
('05670', 'San Roque'),
('05690', 'Santo Domingo'),
('05736', 'Segovia'),
('05858', 'Vegachí'),
('05885', 'Yalí'),
('05890', 'Yolombó'),
('05038', 'Angostura'),
('05086', 'Belmira'),
('05107', 'Briceño'),
('05134', 'Campamento'),
('05150', 'Carolina'),
('05237', 'Don Matias'),
('05264', 'Entrerrios'),
('05310', 'Gómez Plata'),
('05315', 'Guadalupe'),
('05361', 'Ituango'),
('05647', 'San Andrés'),
('05658', 'San José De La Montaña'),
('05664', 'San Pedro'),
('05686', 'Santa Rosa De Osos'),
('05819', 'Toledo'),
('05854', 'Valdivia'),
('05887', 'Yarumal'),
('05004', 'Abriaquí'),
('05044', 'Anza'),
('05059', 'Armenia'),
('05113', 'Buriticá'),
('05138', 'Cañasgordas'),
('05234', 'Dabeiba'),
('05240', 'Ebéjico'),
('05284', 'Frontino'),
('05306', 'Giraldo'),
('05347', 'Heliconia'),
('05411', 'Liborina'),
('05501', 'Olaya'),
('05543', 'Peque'),
('05628', 'Sabanalarga'),
('05656', 'San Jerónimo'),
('05042', 'Santafé De Antioquia'),
('05761', 'Sopetran'),
('05842', 'Uramita'),
('05002', 'Abejorral'),
('05021', 'Alejandría'),
('05055', 'Argelia'),
('05148', 'Carmen De Viboral'),
('05197', 'Cocorná'),
('05206', 'Concepción'),
('05313', 'Granada'),
('05318', 'Guarne'),
('05321', 'Guatape'),
('05376', 'La Ceja'),
('05400', 'La Unión'),
('05440', 'Marinilla'),
('05483', 'Nariño'),
('05541', 'Peñol'),
('05607', 'Retiro'),
('05615', 'Rionegro'),
('05649', 'San Carlos'),
('05652', 'San Francisco'),
('05660', 'San Luis'),
('05667', 'San Rafael'),
('05674', 'San Vicente'),
('05697', 'Santuario'),
('05756', 'Sonson'),
('05030', 'Amaga'),
('05034', 'Andes'),
('05036', 'Angelopolis'),
('05091', 'Betania'),
('05093', 'Betulia'),
('05125', 'Caicedo'),
('05145', 'Caramanta'),
('05101', 'Ciudad Bolívar'),
('05209', 'Concordia'),
('05282', 'Fredonia'),
('05353', 'Hispania'),
('05364', 'Jardín'),
('05368', 'Jericó'),
('05390', 'La Pintada'),
('05467', 'Montebello'),
('05576', 'Pueblorrico'),
('05642', 'Salgar'),
('05679', 'Santa Barbara'),
('05789', 'Támesis'),
('05792', 'Tarso'),
('05809', 'Titiribí'),
('05847', 'Urrao'),
('05856', 'Valparaiso'),
('05861', 'Venecia'),
('05045', 'Apartadó'),
('05051', 'Arboletes'),
('05147', 'Carepa'),
('05172', 'Chigorodó'),
('05475', 'Murindó'),
('05480', 'Mutata'),
('05490', 'Necoclí'),
('05659', 'San Juan De Uraba'),
('05665', 'San Pedro De Uraba'),
('05837', 'Turbo'),
('05873', 'Vigía Del Fuerte'),
('05079', 'Barbosa'),
('05088', 'Bello'),
('05129', 'Caldas'),
('05212', 'Copacabana'),
('05266', 'Envigado'),
('05308', 'Girardota'),
('05360', 'Itagui'),
('05380', 'La Estrella'),
('05001', 'Medellín'),
('05631', 'Sabaneta'),
#ARAUCA
('81001', 'Arauca'),
('81065', 'Arauquita'),
('81220', 'Cravo Norte'),
('81300', 'Fortul'),
('81591', 'Puerto Rondón'),
('81736', 'Saravena'),
('81794', 'Tame'),
#SAN ANDRES
('88564', 'Providencia Y Santa Catalina'),
('88001', 'San Andres'),
#ATLANTICO
('08001', 'Barranquilla'),
('08296', 'Galapa'),
('08433', 'Malambo'),
('08573', 'Puerto Colombia'),
('08758', 'Soledad'),
('08137', 'Campo De La Cruz'),
('08141', 'Candelaria'),
('08421', 'Luruaco'),
('08436', 'Manati'),
('08606', 'Repelon'),
('08675', 'Santa Lucia'),
('08770', 'Suan'),
('08078', 'Baranoa'),
('08520', 'Palmar De Varela'),
('08558', 'Polonuevo'),
('08560', 'Ponedera'),
('08634', 'Sabanagrande'),
('08638', 'Sabanalarga'),
('08685', 'Santo Tomas'),
('08372', 'Juan De Acosta'),
('08549', 'Piojó'),
('08832', 'Tubara'),
('08849', 'Usiacuri'),
#BOGOTA
('11001', 'Bogota D.C.'),
#BOLIVAR
('13188', 'Cicuco'),
('13300', 'Hatillo De Loba'),
('13440', 'Margarita'),
('13468', 'Mompós'),
('13650', 'San Fernando'),
('13780', 'Talaigua Nuevo'),
('13052', 'Arjona'),
('13062', 'Arroyohondo'),
('13140', 'Calamar'),
('13001', 'Cartagena'),
('13222', 'Clemencia'),
('13433', 'Mahates'),
('13620', 'San Cristobal'),
('13647', 'San Estanislao'),
('13673', 'Santa Catalina'),
('13683', 'Santa Rosa De Lima'),
('13760', 'Soplaviento'),
('13836', 'Turbaco'),
('13838', 'Turbana'),
('13873', 'Villanueva'),
('13030', 'Altos Del Rosario'),
('13074', 'Barranco De Loba'),
('13268', 'El Peñon'),
('13580', 'Regidor'),
('13600', 'Río Viejo'),
('13667', 'San Martin De Loba'),
('13042', 'Arenal'),
('13160', 'Cantagallo'),
('13473', 'Morales'),
('13670', 'San Pablo'),
('13688', 'Santa Rosa Del Sur'),
('13744', 'Simití'),
('13006', 'Achí'),
('13430', 'Magangué'),
('13458', 'Montecristo'),
('13549', 'Pinillos'),
('13655', 'San Jacinto Del Cauca'),
('13810', 'Tiquisio'),
('13244', 'Carmen De Bolívar'),
('13212', 'Córdoba'),
('13248', 'El Guamo'),
('13442', 'María La Baja'),
('13654', 'San Jacinto'),
('13657', 'San Juan Nepomuceno'),
('13894', 'Zambrano'),
#BOYACA
('15232', 'Chíquiza'),
('15187', 'Chivatá'),
('15204', 'Cómbita'),
('15224', 'Cucaita'),
('15476', 'Motavita'),
('15500', 'Oicatá'),
('15646', 'Samacá'),
('15740', 'Siachoque'),
('15762', 'Sora'),
('15764', 'Soracá'),
('15763', 'Sotaquirá'),
('15814', 'Toca'),
('15001', 'Tunja'),
('15837', 'Tuta'),
('15861', 'Ventaquemada'),
('15180', 'Chiscas'),
('15223', 'Cubará'),
('15244', 'El Cocuy'),
('15248', 'El Espino'),
('15317', 'Guacamayas'),
('15332', 'Güicán'),
('15522', 'Panqueba'),
('15377', 'Labranzagrande'),
('15518', 'Pajarito'),
('15533', 'Paya'),
('15550', 'Pisba'),
('15090', 'Berbeo'),
('15135', 'Campohermoso'),
('15455', 'Miraflores'),
('15514', 'Páez'),
('15660', 'San Eduardo'),
('15897', 'Zetaquira'),
('15104', 'Boyacá'),
('15189', 'Ciénega'),
('15367', 'Jenesano'),
('15494', 'Nuevo Colón'),
('15599', 'Ramiriquí'),
('15621', 'Rondón'),
('15804', 'Tibaná'),
('15835', 'Turmequé'),
('15842', 'Umbita'),
('15879', 'Viracachá'),
('15172', 'Chinavita'),
('15299', 'Garagoa'),
('15425', 'Macanal'),
('15511', 'Pachavita'),
('15667', 'San Luis De Gaceno'),
('15690', 'Santa María'),
('15097', 'Boavita'),
('15218', 'Covarachía'),
('15403', 'La Uvita'),
('15673', 'San Mateo'),
('15720', 'Sativanorte'),
('15723', 'Sativasur'),
('15753', 'Soatá'),
('15774', 'Susacón'),
('15810', 'Tipacoque'),
('15106', 'Briceño'),
('15109', 'Buenavista'),
('15131', 'Caldas'),
('15176', 'Chiquinquirá'),
('15212', 'Coper'),
('15401', 'La Victoria'),
('15442', 'Maripí'),
('15480', 'Muzo'),
('15507', 'Otanche'),
('15531', 'Pauna'),
('15572', 'Puerto Boyaca'),
('15580', 'Quípama'),
('15632', 'Saboyá'),
('15676', 'San Miguel De Sema'),
('15681', 'San Pablo Borbur'),
('15832', 'Tununguá'),
('15022', 'Almeida'),
('15236', 'Chivor'),
('15322', 'Guateque'),
('15325', 'Guayatá'),
('15380', 'La Capilla'),
('15761', 'Somondoco'),
('15778', 'Sutatenza'),
('15798', 'Tenza'),
('15051', 'Arcabuco'),
('15185', 'Chitaraque'),
('15293', 'Gachantivá'),
('15469', 'Moniquirá'),
('15600', 'Ráquira'),
('15638', 'Sáchica'),
('15664', 'San José De Pare'),
('15696', 'Santa Sofía'),
('15686', 'Santana'),
('15776', 'Sutamarchán'),
('15808', 'Tinjacá'),
('15816', 'Togüí'),
('15407', 'Villa De Leyva'),
('15047', 'Aquitania'),
('15226', 'Cuítiva'),
('15272', 'Firavitoba'),
('15296', 'Gameza'),
('15362', 'Iza'),
('15464', 'Mongua'),
('15466', 'Monguí'),
('15491', 'Nobsa'),
('15542', 'Pesca'),
('15759', 'Sogamoso'),
('15806', 'Tibasosa'),
('15820', 'Tópaga'),
('15822', 'Tota'),
('15087', 'Belén'),
('15114', 'Busbanzá'),
('15162', 'Cerinza'),
('15215', 'Corrales'),
('15238', 'Duitama'),
('15276', 'Floresta'),
('15516', 'Paipa'),
('15693', 'San Rosa Viterbo'),
('15839', 'Tutazá'),
('15092', 'Betéitiva'),
('15183', 'Chita'),
('15368', 'Jericó'),
('15537', 'Paz De Río'),
('15757', 'Socha'),
('15755', 'Socotá'),
('15790', 'Tasco'),
('', ''),
('17272', 'Filadelfia'),
('17388', 'La Merced'),
('17442', 'Marmato'),
('17614', 'Riosucio'),
('17777', 'Supía'),
('17433', 'Manzanares'),
('17444', 'Marquetalia'),
('17446', 'Marulanda'),
('17541', 'Pensilvania'),
('17042', 'Anserma'),
('17088', 'Belalcázar'),
('17616', 'Risaralda'),
('17665', 'San José'),
('17877', 'Viterbo'),
('17174', 'Chinchina'),
('17001', 'Manizales'),
('17486', 'Neira'),
('17524', 'Palestina'),
('17873', 'Villamaria'),
('17013', 'Aguadas'),
('17050', 'Aranzazu'),
('17513', 'Pácora'),
('17653', 'Salamina'),
('17380', 'La Dorada'),
('17495', 'Norcasia'),
('17662', 'Samaná'),
('17867', 'Victoria'),
#CAQUETA
('18029', 'Albania'),
('18094', 'Belén De Los Andaquies'),
('18150', 'Cartagena Del Chairá'),
('18205', 'Currillo'),
('18247', 'El Doncello'),
('18256', 'El Paujil'),
('18001', 'Florencia'),
('18410', 'La Montañita'),
('18460', 'Milan'),
('18479', 'Morelia'),
('18592', 'Puerto Rico'),
('18610', 'San Jose Del Fragua'),
('18753', 'San Vicente Del Caguán'),
('18756', 'Solano'),
('18785', 'Solita'),
('18860', 'Valparaiso'),
#CASANARE
('85010', 'Aguazul'),
('85015', 'Chameza'),
('85125', 'Hato Corozal'),
('85136', 'La Salina'),
('85139', 'Maní'),
('85162', 'Monterrey'),
('85225', 'Nunchía'),
('85230', 'Orocué'),
('85250', 'Paz De Ariporo'),
('85263', 'Pore'),
('85279', 'Recetor'),
('85300', 'Sabanalarga'),
('85315', 'Sácama'),
('85325', 'San Luis De Palenque'),
('85400', 'Támara'),
('85410', 'Tauramena'),
('85430', 'Trinidad'),
('85440', 'Villanueva'),
('85001', 'Yopal'),
#CAUCA
('19130', 'Cajibío'),
('19256', 'El Tambo'),
('19392', 'La Sierra'),
('19473', 'Morales'),
('19548', 'Piendamo'),
('19001', 'Popayán'),
('19622', 'Rosas'),
('19760', 'Sotara'),
('19807', 'Timbio'),
('19110', 'Buenos Aires'),
('19142', 'Caloto'),
('19212', 'Corinto'),
('19455', 'Miranda'),
('19513', 'Padilla'),
('19573', 'Puerto Tejada'),
('19698', 'Santander De Quilichao'),
('19780', 'Suarez'),
('19845', 'Villa Rica'),
('19318', 'Guapi'),
('19418', 'Lopez'),
('19809', 'Timbiqui'),
('19137', 'Caldono'),
('19355', 'Inzá'),
('19364', 'Jambalo'),
('19517', 'Paez'),
('19585', 'Purace'),
('19743', 'Silvia'),
('19821', 'Toribio'),
('19824', 'Totoro'),
('19022', 'Almaguer'),
('19050', 'Argelia'),
('19075', 'Balboa'),
('19100', 'Bolívar'),
('19290', 'Florencia'),
('19397', 'La Vega'),
('19450', 'Mercaderes'),
('19532', 'Patia'),
('19533', 'Piamonte'),
('19693', 'San Sebastian'),
('19701', 'Santa Rosa'),
('19785', 'Sucre'),
#CESAR
('20045', 'Becerril'),
('20175', 'Chimichagua'),
('20178', 'Chiriguana'),
('20228', 'Curumaní'),
('20400', 'La Jagua De Ibirico'),
('20517', 'Pailitas'),
('20787', 'Tamalameque'),
('20032', 'Astrea'),
('20060', 'Bosconia'),
('20238', 'El Copey'),
('20250', 'El Paso'),
('20013', 'Agustín Codazzi'),
('20621', 'La Paz'),
('20443', 'Manaure'),
('20570', 'Pueblo Bello'),
('20750', 'San Diego'),
('20001', 'Valledupar'),
('20011', 'Aguachica'),
('20295', 'Gamarra'),
('20310', 'González'),
('20383', 'La Gloria'),
('20550', 'Pelaya'),
('20614', 'Río De Oro'),
('20710', 'San Alberto'),
('20770', 'San Martín'),
#CHOCO
('27050', 'Atrato'),
('27073', 'Bagadó'),
('27099', 'Bojaya'),
('27245', 'El Carmen De Atrato'),
('27413', 'Lloró'),
('27425', 'Medio Atrato'),
('27001', 'Quibdó'),
('27600', 'Rio Quito'),
('27006', 'Acandí'),
('27086', 'Belén De Bajira'),
('27150', 'Carmén Del Darién'),
('27615', 'Riosucio'),
('27800', 'Unguía'),
('27075', 'Bahía Solano'),
('27372', 'Juradó'),
('27495', 'Nuquí'),
('27025', 'Alto Baudó'),
('27077', 'Bajo Baudó'),
('27250', 'El Litoral Del San Juan'),
('27430', 'Medio Baudó'),
('27135', 'Canton De San Pablo'),
('27160', 'Certegui'),
('27205', 'Condoto'),
('27361', 'Itsmina'),
('27450', 'Medio San Juan'),
('27491', 'Nóvita'),
('27580', 'Río Frío'),
('27660', 'San José Del Palmar'),
('27745', 'Sipí'),
('27787', 'Tadó'),
('27810', 'Union Panamericana'),
#CORDOBA
('23807', 'Tierralta'),
('23855', 'Valencia'),
('23168', 'Chimá'),
('23300', 'Cotorra'),
('23417', 'Lorica'),
('23464', 'Momil'),
('23586', 'Purísima'),
('23001', 'Montería'),
('23090', 'Canalete'),
('23419', 'Los Córdobas'),
('23500', 'Moñitos'),
('23574', 'Puerto Escondido'),
('23672', 'San Antero'),
('23675', 'San Bernardo Del Viento'),
('23182', 'Chinú'),
('23660', 'Sahagún'),
('23670', 'San Andrés Sotavento'),
('23068', 'Ayapel'),
('23079', 'Buenavista'),
('23350', 'La Apartada'),
('23466', 'Montelíbano'),
('23555', 'Planeta Rica'),
('23570', 'Pueblo Nuevo'),
('23580', 'Puerto Libertador'),
('23162', 'Cereté'),
('23189', 'Ciénaga De Oro'),
('23678', 'San Carlos'),
('23686', 'San Pelayo'),
#CUNDINAMARCA
('25183', 'Chocontá'),
('25426', 'Macheta'),
('25436', 'Manta'),
('25736', 'Sesquilé'),
('25772', 'Suesca'),
('25807', 'Tibirita'),
('25873', 'Villapinzón'),
('25001', 'Agua De Dios'),
('25307', 'Girardot'),
('25324', 'Guataquí'),
('25368', 'Jerusalén'),
('25483', 'Nariño'),
('25488', 'Nilo'),
('25612', 'Ricaurte'),
('25815', 'Tocaima'),
('25148', 'Caparrapí'),
('25320', 'Guaduas'),
('25572', 'Puerto Salgar'),
('25019', 'Albán'),
('25398', 'La Peña'),
('25402', 'La Vega'),
('25489', 'Nimaima'),
('25491', 'Nocaima'),
('25592', 'Quebradanegra'),
('25658', 'San Francisco'),
('25718', 'Sasaima'),
('25777', 'Supatá'),
('25851', 'Útica'),
('25862', 'Vergara'),
('25875', 'Villeta'),
('25293', 'Gachala'),
('25297', 'Gacheta'),
('25299', 'Gama'),
('25322', 'Guasca'),
('25326', 'Guatavita'),
('25372', 'Junín'),
('25377', 'La Calera'),
('25839', 'Ubalá'),
('25086', 'Beltrán'),
('25095', 'Bituima'),
('25168', 'Chaguaní'),
('25328', 'Guayabal De Siquima'),
('25580', 'Puli'),
('25662', 'San Juan De Río Seco'),
('25867', 'Vianí'),
('25438', 'Medina'),
('25530', 'Paratebueno'),
('25151', 'Caqueza'),
('25178', 'Chipaque'),
('25181', 'Choachí'),
('25279', 'Fomeque'),
('25281', 'Fosca'),
('25335', 'Guayabetal'),
('25339', 'Gutiérrez'),
('25594', 'Quetame'),
('25841', 'Ubaque'),
('25845', 'Une'),
('25258', 'El Peñón'),
('25394', 'La Palma'),
('25513', 'Pacho'),
('25518', 'Paime'),
('25653', 'San Cayetano'),
('25823', 'Topaipi'),
('25871', 'Villagomez'),
('25885', 'Yacopí'),
('25126', 'Cajicá'),
('25175', 'Chía'),
('25200', 'Cogua'),
('25295', 'Gachancipá'),
('25486', 'Nemocon'),
('25758', 'Sopó'),
('25785', 'Tabio'),
('25817', 'Tocancipá'),
('25899', 'Zipaquirá'),
('25099', 'Bojacá'),
('25214', 'Cota'),
('25260', 'El Rosal'),
('25269', 'Facatativá'),
('25286', 'Funza'),
('25430', 'Madrid'),
('25473', 'Mosquera'),
('25769', 'Subachoque'),
('25799', 'Tenjo'),
('25898', 'Zipacon'),
('25740', 'Sibaté'),
('25754', 'Soacha'),
('25053', 'Arbeláez'),
('25120', 'Cabrera'),
('25290', 'Fusagasugá'),
('25312', 'Granada'),
('25524', 'Pandi'),
('25535', 'Pasca'),
('25649', 'San Bernardo'),
('25743', 'Silvania'),
('25805', 'Tibacuy'),
('25506', 'Venecia'),
('25035', 'Anapoima'),
('25040', 'Anolaima'),
('25599', 'Apulo'),
('25123', 'Cachipay'),
('25245', 'El Colegio'),
('25386', 'La Mesa'),
('25596', 'Quipile'),
('25645', 'San Antonio De Tequendama'),
('25797', 'Tena'),
('25878', 'Viotá'),
('25154', 'Carmen De Carupa'),
('25224', 'Cucunubá'),
('25288', 'Fúquene'),
('25317', 'Guachetá'),
('25407', 'Lenguazaque'),
('25745', 'Simijaca'),
('25779', 'Susa'),
('25781', 'Sutatausa'),
('25793', 'Tausa'),
('25843', 'Ubate'),
#GUAINIA
('94343', 'Barranco Mina'),
('94886', 'Cacahual'),
('94001', 'Inírida'),
('94885', 'La Guadalupe'),
('94663', 'Mapiripan'),
('94888', 'Morichal'),
('94887', 'Pana Pana'),
('94884', 'Puerto Colombia'),
('94883', 'San Felipe'),
#GUAVIARE
('95015', 'Calamar'),
('95025', 'El Retorno'),
('95200', 'Miraflores'),
('95001', 'San José Del Guaviare'),
#HUILA
('41013', 'Agrado'),
('41026', 'Altamira'),
('41298', 'Garzón'),
('41306', 'Gigante'),
('41319', 'Guadalupe'),
('41548', 'Pital'),
('41770', 'Suaza'),
('41791', 'Tarqui'),
('41016', 'Aipe'),
('41020', 'Algeciras'),
('41078', 'Baraya'),
('41132', 'Campoalegre'),
('41206', 'Colombia'),
('41349', 'Hobo'),
('41357', 'Iquira'),
('41001', 'Neiva'),
('41524', 'Palermo'),
('41615', 'Rivera'),
('41676', 'Santa María'),
('41799', 'Tello'),
('41801', 'Teruel'),
('41872', 'Villavieja'),
('41885', 'Yaguará'),
('41378', 'La Argentina'),
('41396', 'La Plata'),
('41483', 'Nátaga'),
('41518', 'Paicol'),
('41797', 'Tesalia'),
('41006', 'Acevedo'),
('41244', 'Elías'),
('41359', 'Isnos'),
('41503', 'Oporapa'),
('41530', 'Palestina'),
('41551', 'Pitalito'),
('41660', 'Saladoblanco'),
('41668', 'San Agustín'),
('41807', 'Timaná'),
#LA GUAJIRA
('44035', 'Albania'),
('44090', 'Dibulla'),
('44430', 'Maicao'),
('44560', 'Manaure'),
('44001', 'Riohacha'),
('44847', 'Uribia'),
('44078', 'Barrancas'),
('44098', 'Distraccion'),
('44110', 'El Molino'),
('44279', 'Fonseca'),
('44378', 'Hatonuevo'),
('44420', 'La Jagua Del Pilar'),
('44650', 'San Juan Del Cesar'),
('44855', 'Urumita'),
('44874', 'Villanueva'),
#MAGDALENA
('47058', 'Ariguaní'),
('47170', 'Chibolo'),
('47460', 'Nueva Granada'),
('47555', 'Plato'),
('47660', 'Sabanas De San Angel'),
('47798', 'Tenerife'),
('47030', 'Algarrobo'),
('47053', 'Aracataca'),
('47189', 'Ciénaga'),
('47268', 'El Reten'),
('47288', 'Fundacion'),
('47570', 'Pueblo Viejo'),
('47980', 'Zona Bananera'),
('47161', 'Cerro San Antonio'),
('47205', 'Concordia'),
('47258', 'El Piñon'),
('47541', 'Pedraza'),
('47551', 'Pivijay'),
('47605', 'Remolino'),
('47675', 'Salamina'),
('47745', 'Sitionuevo'),
('47960', 'Zapayan'),
('47001', 'Santa Marta'),
('47245', 'El Banco'),
('47318', 'Guamal'),
('47545', 'Pijiño Del Carmen'),
('47692', 'San Sebastian De Buenavista'),
('47703', 'San Zenon'),
('47707', 'Santa Ana'),
('47720', 'Santa Barbara De Pinto'),
#META
('50251', 'El Castillo'),
('50270', 'El Dorado'),
('50287', 'Fuente De Oro'),
('50313', 'Granada'),
('50350', 'La Macarena'),
('50370', 'La Uribe'),
('50400', 'Lejanías'),
('50325', 'Mapiripan'),
('50330', 'Mesetas'),
('50450', 'Puerto Concordia'),
('50577', 'Puerto Lleras'),
('50590', 'Puerto Rico'),
('50683', 'San Juan De Arama'),
('50711', 'Vista Hermosa'),
('50001', 'Villavicencio'),
('50006', 'Acacias'),
('50110', 'Barranca De Upia'),
('50150', 'Castilla La Nueva'),
('50226', 'Cumaral'),
('50245', 'El Calvario'),
('50318', 'Guamal'),
('50606', 'Restrepo'),
('50680', 'San Carlos Guaroa'),
('50686', 'San Juanito'),
('50223', 'San Luis De Cubarral'),
('50689', 'San Martín'),
('50124', 'Cabuyaro'),
('50568', 'Puerto Gaitán'),
('50573', 'Puerto Lopez'),
#NARIÑO
('52240', 'Chachagui'),
('52207', 'Consaca'),
('52254', 'El Peñol'),
('52260', 'El Tambo'),
('52381', 'La Florida'),
('52480', 'Nariño'),
('52001', 'Pasto'),
('52683', 'Sandoná'),
('52788', 'Tangua'),
('52885', 'Yacuanquer'),
('52036', 'Ancuya'),
('52320', 'Guaitarilla'),
('52385', 'La Llanada'),
('52411', 'Linares'),
('52418', 'Los Andes'),
('52435', 'Mallama'),
('52506', 'Ospina'),
('52565', 'Providencia'),
('52612', 'Ricaurte'),
('52678', 'Samaniego'),
('52699', 'Santa Cruz'),
('52720', 'Sapuyes'),
('52838', 'Tuquerres'),
('52079', 'Barbacoas'),
('52250', 'El Charco'),
('52520', 'Francisco Pizarro'),
('52390', 'La Tola'),
('52427', 'Magui'),
('52473', 'Mosquera'),
('52490', 'Olaya Herrera'),
('52621', 'Roberto Payan'),
('52696', 'Santa Barbara'),
('52835', 'Tumaco'),
('52019', 'Alban'),
('52051', 'Arboleda'),
('52083', 'Belen'),
('52110', 'Buesaco'),
('52203', 'Colon'),
('52233', 'Cumbitara'),
('52256', 'El Rosario'),
('52258', 'El Tablon De Gomez'),
('52378', 'La Cruz'),
('52399', 'La Union'),
('52405', 'Leiva'),
('52540', 'Policarpa'),
('52685', 'San Bernardo'),
('52687', 'San Lorenzo'),
('52693', 'San Pablo'),
('52694', 'San Pedro De Cartago'),
('52786', 'Taminango'),
('52022', 'Aldana'),
('52210', 'Contadero'),
('52215', 'Córdoba'),
('52224', 'Cuaspud'),
('52227', 'Cumbal'),
('52287', 'Funes'),
('52317', 'Guachucal'),
('52323', 'Gualmatan'),
('52352', 'Iles'),
('52354', 'Imues'),
('52356', 'Ipiales'),
('52560', 'Potosí'),
('52573', 'Puerres'),
('52585', 'Pupiales'),
#NORTE DE SANTANDER
('54051', 'Arboledas'),
('54223', 'Cucutilla'),
('54313', 'Gramalote'),
('54418', 'Lourdes'),
('54660', 'Salazar'),
('54680', 'Santiago'),
('54871', 'Villa Caro'),
('54109', 'Bucarasica'),
('54250', 'El Tarra'),
('54720', 'Sardinata'),
('54810', 'Tibú'),
('54003', 'Abrego'),
('54128', 'Cachirá'),
('54206', 'Convención'),
('54245', 'El Carmen'),
('54344', 'Hacarí'),
('54385', 'La Esperanza'),
('54398', 'La Playa'),
('54498', 'Ocaña'),
('54670', 'San Calixto'),
('54800', 'Teorama'),
('54001', 'Cúcuta'),
('54261', 'El Zulia'),
('54405', 'Los Patios'),
('54553', 'Puerto Santander'),
('54673', 'San Cayetano'),
('54874', 'Villa Del Rosario'),
('54125', 'Cácota'),
('54174', 'Chitagá'),
('54480', 'Mutiscua'),
('54518', 'Pamplona'),
('54520', 'Pamplonita'),
('54743', 'Silos'),
('54099', 'Bochalema'),
('54172', 'Chinácota'),
('54239', 'Durania'),
('54347', 'Herrán'),
('54377', 'Labateca'),
('54599', 'Ragonvalia'),
('54820', 'Toledo'),
#PUTUMAYO
('86219', 'Colón'),
('86001', 'Mocoa'),
('86320', 'Orito'),
('86568', 'Puerto Asis'),
('86569', 'Puerto Caicedo'),
('86571', 'Puerto Guzman'),
('86573', 'Puerto Leguizamo'),
('86755', 'San Francisco'),
('86757', 'San Miguel'),
('86760', 'Santiago'),
('86749', 'Sibundoy'),
('86865', 'Valle Del Guamuez'),
('86885', 'Villa Garzon'),
#QUINDIO
('63001', 'Armenia'),
('63111', 'Buenavista'),
('63130', 'Calarca'),
('63212', 'Cordoba'),
('63302', 'Genova'),
('63548', 'Pijao'),
('63272', 'Filandia'),
('63690', 'Salento'),
('63190', 'Circasia'),
('63401', 'La Tebaida'),
('63470', 'Montengro'),
('63594', 'Quimbaya'),
#RISARALDA
('66170', 'Dosquebradas'),
('66400', 'La Virginia'),
('66440', 'Marsella'),
('66001', 'Pereira'),
('66682', 'Santa Rosa De Cabal'),
('66045', 'Apía'),
('66075', 'Balboa'),
('66088', 'Belén De Umbría'),
('66318', 'Guática'),
('66383', 'La Celia'),
('66594', 'Quinchia'),
('66687', 'Santuario'),
('66456', 'Mistrató'),
('66572', 'Pueblo Rico'),
#SANTANDER
('68176', 'Chima'),
('68209', 'Confines'),
('68211', 'Contratación'),
('68245', 'El Guacamayo'),
('68296', 'Galán'),
('68298', 'Gambita'),
('68320', 'Guadalupe'),
('68322', 'Guapotá'),
('68344', 'Hato'),
('68500', 'Oiba'),
('68522', 'Palmar'),
('68524', 'Palmas Del Socorro'),
('68720', 'Santa Helena Del Opón'),
('68745', 'Simacota'),
('68755', 'Socorro'),
('68770', 'Suaita'),
('68147', 'Capitanejo'),
('68152', 'Carcasí'),
('68160', 'Cepitá'),
('68162', 'Cerrito'),
('68207', 'Concepción'),
('68266', 'Enciso'),
('68318', 'Guaca'),
('68425', 'Macaravita'),
('68432', 'Málaga'),
('68468', 'Molagavita'),
('68669', 'San Andrés'),
('68684', 'San José De Miranda'),
('68686', 'San Miguel'),
('68051', 'Aratoca'),
('68079', 'Barichara'),
('68121', 'Cabrera'),
('68167', 'Charalá'),
('68217', 'Coromoro'),
('68229', 'Curití'),
('68264', 'Encino'),
('68370', 'Jordán'),
('68464', 'Mogotes'),
('68498', 'Ocamonte'),
('68502', 'Onzaga'),
('68533', 'Páramo'),
('68549', 'Pinchote'),
('68679', 'San Gil'),
('68682', 'San Joaquín'),
('68855', 'Valle De San José'),
('68872', 'Villanueva'),
('68081', 'Barrancabermeja'),
('68092', 'Betulia'),
('68235', 'El Carmen De Chucurí'),
('68575', 'Puerto Wilches'),
('68655', 'Sabana De Torres'),
('68689', 'San Vicente De Chucurí'),
('68895', 'Zapatoca'),
('68001', 'Bucaramanga'),
('68132', 'California'),
('68169', 'Charta'),
('68255', 'El Playón'),
('68276', 'Floridablanca'),
('68307', 'Girón'),
('68406', 'Lebríja'),
('68418', 'Los Santos'),
('68444', 'Matanza'),
('68547', 'Piedecuesta'),
('68615', 'Rionegro'),
('68705', 'Santa Bárbara'),
('68780', 'Surata'),
('68820', 'Tona'),
('68867', 'Vetas'),
('68013', 'Aguada'),
('68020', 'Albania'),
('68077', 'Barbosa'),
('68101', 'Bolívar'),
('68179', 'Chipatá'),
('68190', 'Cimitarra'),
('68250', 'El Peñón'),
('68271', 'Florián'),
('68324', 'Guavatá'),
('68327', 'Guepsa'),
('68368', 'Jesús María'),
('68377', 'La Belleza'),
('68397', 'La Paz'),
('68385', 'Landázuri'),
('68572', 'Puente Nacional'),
('68573', 'Puerto Parra'),
('68673', 'San Benito'),
('68773', 'Sucre'),
('68861', 'Vélez'),
#SUCRE
('70265', 'Guaranda'),
('70429', 'Majagual'),
('70771', 'Sucre'),
('70230', 'Chalán'),
('70204', 'Coloso'),
('70473', 'Morroa'),
('70508', 'Ovejas'),
('70001', 'Sincelejo'),
('70221', 'Coveñas'),
('70523', 'Palmito'),
('70713', 'San Onofre'),
('70820', 'Santiago De Tolú'),
('70823', 'Tolú Viejo'),
('70110', 'Buenavista'),
('70215', 'Corozal'),
('70233', 'El Roble'),
('70235', 'Galeras'),
('70418', 'Los Palmitos'),
('70670', 'Sampués'),
('70702', 'San Juan Betulia'),
('70717', 'San Pedro'),
('70742', 'Sincé'),
('70124', 'Caimito'),
('70400', 'La Unión'),
('70678', 'San Benito Abad'),
('70708', 'San Marcos'),
#TOLIMA
('73030', 'Ambalema'),
('73055', 'Armero'),
('73270', 'Falan'),
('73283', 'Fresno'),
('73349', 'Honda'),
('73443', 'Mariquita'),
('73520', 'Palocabildo'),
('73148', 'Carmen De Apicalá'),
('73226', 'Cunday'),
('73352', 'Icononzo'),
('73449', 'Melgar'),
('73873', 'Villarrica'),
('73067', 'Ataco'),
('73168', 'Chaparral'),
('73217', 'Coyaima'),
('73483', 'Natagaima'),
('73504', 'Ortega'),
('73555', 'Planadas'),
('73616', 'Rioblanco'),
('73622', 'Roncesvalles'),
('73675', 'San Antonio'),
('73026', 'Alvarado'),
('73043', 'Anzoátegui'),
('73124', 'Cajamarca'),
('73200', 'Coello'),
('73268', 'Espinal'),
('73275', 'Flandes'),
('73001', 'Ibague'),
('73547', 'Piedras'),
('73624', 'Rovira'),
('73678', 'San Luis'),
('73854', 'Valle De San Juan'),
('73024', 'Alpujarra'),
('73236', 'Dolores'),
('73319', 'Guamo'),
('73563', 'Prado'),
('73585', 'Purificación'),
('73671', 'Saldaña'),
('73770', 'Suárez'),
('73152', 'Casabianca'),
('73347', 'Herveo'),
('73408', 'Lerida'),
('73411', 'Libano'),
('73461', 'Murillo'),
('73686', 'Santa Isabel'),
('73861', 'Venadillo'),
('73870', 'Villahermosa'),
#VALLE DEL CAUCA
('76036', 'Andalucía'),
('76111', 'Buga'),
('76113', 'Bugalagrande'),
('76126', 'Calima'),
('76248', 'El Cerrito'),
('76306', 'Ginebra'),
('76318', 'Guacarí'),
('76606', 'Restrepo'),
('76616', 'Riofrio'),
('76670', 'San Pedro'),
('76828', 'Trujillo'),
('76834', 'Tuluá'),
('76890', 'Yotoco'),
('76020', 'Alcala'),
('76041', 'Ansermanuevo'),
('76054', 'Argelia'),
('76100', 'Bolívar'),
('76147', 'Cartago'),
('76243', 'El Águila'),
('76246', 'El Cairo'),
('76250', 'El Dovio'),
('76400', 'La Unión'),
('76403', 'La Victoria'),
('76497', 'Obando'),
('76622', 'Roldanillo'),
('76823', 'Toro'),
('76845', 'Ulloa'),
('76863', 'Versalles'),
('76895', 'Zarzal'),
('76109', 'Buenaventura'),
('76122', 'Caicedonia'),
('76736', 'Sevilla'),
('76001', 'Cali'),
('76130', 'Candelaria'),
('76233', 'Dagua'),
('76275', 'Florida'),
('76364', 'Jamundí'),
('76377', 'La Cumbre'),
('76520', 'Palmira'),
('76563', 'Pradera'),
('76869', 'Vijes'),
('76892', 'Yumbo'),
#VAUPES
('97161', 'Caruru'),
('97001', 'Mitú'),
('97511', 'Pacoa'),
('97777', 'Papunahua'),
('97666', 'Taraira'),
('97889', 'Yavaraté'),
#VICHADA
('99773', 'Cumaribo'),
('99524', 'La Primavera'),
('99001', 'Puerto Carreño'),
('99624', 'Santa Rosalía'),
)
class Paises(models.Model):
    nombre = models.CharField(max_length=50, db_column='T003nombre')
    cod_pais = models.CharField(primary_key=True,max_length=2, db_column='T003CodPais')
    def __str__(self):
        return self.cod_pais
    class Meta:
        db_table = "T003Paises"
        verbose_name='Pais'
        verbose_name_plural='Paises'
        

class EstadoCivil (models.Model):
    nombre = models.CharField(max_length=20, db_column='T005nombre')
    cod_estado_civil = models.CharField(primary_key=True,max_length=1, db_column='T005CodEstadoCivil')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T005EstadoCivil'
        verbose_name='Estado civil'
        verbose_name_plural='Estado civil'

class Departamento (models.Model):
    nombre = models.CharField(max_length=30, db_column='T002nombre')
    pais = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T002Cod_Pais')
    cod_departamento = models.CharField(primary_key=True, max_length=2, db_column='T002CodDepartamento')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T002DepartamentosPais'
        verbose_name='Departamento'
        verbose_name_plural='Departamentos'



class Municipio (models.Model):
    nombre = models.CharField(max_length=30, db_column='T001nombre')
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='T001Cod_Departamentos')
    cod_municipio = models.CharField(primary_key=True, max_length=5, db_column = 'T001CodMunicipio')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T001MunicipiosDepartamento'
        verbose_name='Municipio'
        verbose_name_plural='Municipios'


class Permisos(models.Model):
    
    class cod_permiso_CHOICES(models.TextChoices):
        crear = "CR", "Crear"
        borrar = "BO", "Borrar"
        actualizar= "CO","Consultar"
        ejecutar="EJ","Ejecutar"
        aprobar="AP","Aprobar"
        
    nombre_permiso = models.CharField(max_length=20, db_column='TznombrePermiso')
    cod_permiso = models.CharField(max_length=2,primary_key=True, editable=False,choices=cod_permiso_CHOICES.choices, db_column='TzCodPermiso')

    def __str__(self):
        return self.nombre_permiso

    class Meta:
        db_table = "TzPermisos"
        verbose_name='Permiso'
        verbose_name_plural='Permisos'

class OperacionesSobreUsuario(models.Model):
    cod_operacion = models.AutoField(primary_key=True, editable=False, db_column='T008CodOperacion')
    nombre = models.CharField(max_length=20, db_column='T008nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T008OperacionesSobreUsusario'
        verbose_name='Operacion sobre usuario'
        verbose_name_plural='Operaciones sobre usuario'

class TiposDocumento(models.Model):
    cod_tipo_documento = models.AutoField(primary_key=True, editable=False, db_column='T006CodTipoDocumento')
    nombre = models.CharField(max_length=40, db_column='T006nombre')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'T006TiposDocumento'
        verbose_name='Tipo de documento'
        verbose_name_plural='Tipos de documento'

    
class Roles(models.Model):
    id_rol=models.AutoField(primary_key=True, editable=False, db_column='TzIdRol')
    nombre_rol=models.CharField(max_length=100, db_column='TznombreRol')
    descripcion_rol=models.CharField(max_length=255,db_column='TzdescripcionRol')
    
    class Meta:
        db_table= 'TzRoles'
        verbose_name='Rol'
        verbose_name_plural='Roles'
        
    def __str__(self):
         return self.nombre_rol
    
        
class Modulos(models.Model):
    class subsistema_CHOICES(models.TextChoices):
        conservacion="CONS","Conservación"
        gestion_Documental="GEST","Gestión Documental"
        recurso_hidrico="RECU","Recurso Hídrico"
        tramites_servicio="TRAM","Trámites y servicios"
        seguimiento_planes="PLAN","Seguimiento a planes"
        recaudo="RECA","Recaudo"
        
    id_modulo=models.AutoField(primary_key=True, editable=False, db_column='TzIdModulo')
    nombre_modulo=models.CharField(max_length=70,db_column='TznombreModulo')
    subsistema=models.CharField(max_length=4,choices=subsistema_CHOICES.choices,db_column='Tzsubsistema')# Juan camilo textchoices 
    descripcion = models.CharField(max_length=255, db_column='Tzdescripcion')
    
    class Meta:
        db_table= 'TzModulos'
        verbose_name='Modulo'
        verbose_name_plural='Modulos'
        
    def __str__(self):
         return self.nombre_modulo

class PermisosModulo(models.Model):
    
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzIdModulo')
    cod_permiso=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCodPermiso') #juan Camilo Text Choices
  
    class Meta:
        db_table= 'TzPermisos_Modulo'
        verbose_name='Permiso de módulo'
        verbose_name_plural='Permisos de módulo'

class PermisosModuloRol(models.Model):
    id_rol=models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='TzIdRol')
    id_modulo=models.ForeignKey(PermisosModulo, on_delete=models.CASCADE, db_column='TzIdModulo')
    cod_permiso=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCodPermiso')
    
    class Meta:
        db_table= 'TzPermisos_Modulo_Rol'
        verbose_name='Permiso de modulo de rol'
        verbose_name_plural='Permisos de modulo de roles'
    
class Personas(models.Model):
    class Sexo(models.TextChoices):
        Hombre = "H", "Hombre"
        Mujer = "M", "Mujer"
        InterSexual = "I", "Intersexual"  
    class EstadoCivil(models.TextChoices):
        Casado = "C", "Casado"
        Soltero = "S", "soltero"
        UnionLibre = "U", "Unión Libre"
        Viudo = "V", "Viudo"
        Divorciado = "D", "Divorciado"
    class TiposDocumento(models.TextChoices):
        NUIP = "UN", "NUIP"
        CedulaExtrangeria = "CE", "Cédula Extrangeria"
        Pasaporte = "PA", "Pasaporte"
        PermisoEspecialDePermanencia = "PE", "Permiso Especial de Permanencia"
        RegistroCivil = "RC", "Registro Civil"
        TarjetaDeIdentidad = "TI", "Tarjeta de Identidad"
        CedulaDeCiudadania = "CC", "Cédula de Ciudadania"

    class TipoPersona(models.TextChoices):
        Natural = "N", "Natural"
        Juridica = "J", "Juridica"

    id_persona = models.AutoField(primary_key=True, editable=False, db_column='T010IdPersona')
    tipo_persona = models.CharField(max_length=1, choices=TipoPersona.choices, db_column='T010tipoPersona')
    tipo_documento = models.CharField(max_length=2, choices=TiposDocumento.choices, db_column='T010Cod_TipoDocumento')
    numero_documento = models.CharField(max_length=20, unique=True, db_column='T010nroDocumento')
    digito_verificacion = models.CharField(max_length=1, null=True, blank=True, db_column='T010digitoVerificacion')
    primer_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerNombre')
    segundo_nombre = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoNombre')
    primer_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010primerApellido')
    segundo_apellido = models.CharField(max_length=30, null=True, blank=True, db_column='T010segundoApellido')
    nombre_comercial = models.CharField(max_length=200, null=True, blank=True, db_column='T010nombreComercial')
    razon_social = models.CharField(max_length=200, null=True, blank=True, db_column='T010razonSocial')
    pais_residencia = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010codPaisResidencia')
    departamento_residencia = models.CharField(max_length=2, choices=departamentos_CHOICES, db_column='T010codDepartamentoResidencia')
    municipio_residencia = models.CharField(max_length=5,choices=municipios_CHOICES, null=True, blank=True, db_column='T010Cod_MunicipioResidenciaNal')
    direccion_residencia = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidencia')
    direccion_residencia_ref = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirResidenciaReferencia')
    ubicacion_georeferenciada = models.CharField(max_length=50, db_column='T010ubicacionGeoreferenciada')
    direccion_laboral = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirLaboralNal')
    direccion_notificaciones = models.CharField(max_length=255, null=True, blank=True, db_column='T010dirNotificacion')
    pais_nacimiento = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010Cod_Pais_Nacimiento')
    fecha_nacimiento = models.DateField(blank=True,null=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, db_column='T010Cod_Sexo')
    estado_civil = models.CharField(max_length=1, choices=EstadoCivil.choices, null=True, blank=True, db_column='T010Cod_Estado_Civil')
    representante_legal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,blank=True, db_column='T010Id_PersonaRepLegal')
    email = models.EmailField(max_length=255, unique=True, db_column='T010emailNotificación')
    email_empresarial = models.EmailField(max_length=255, null=True, blank=True, db_column='T010emailEmpresarial')
    telefono_fijo_residencial = models.CharField(max_length=15, null=True, blank=True, db_column='T010telFijoResidencial')
    telefono_celular = models.CharField(max_length=15, null=True, blank=True, db_column='T010telCelular')
    telefono_empresa = models.CharField(max_length=15, null=True, blank=True, db_column='T010telEmpresa')
    cod_municipio_laboral_nal = models.CharField(max_length=5, choices=municipios_CHOICES, null=True, blank=True, db_column='T010Cod_MunicipioLaboralNal')
    cod_municipio_notificacion_nal = models.CharField(max_length=5, choices=municipios_CHOICES, null=True, blank=True, db_column='T010Cod_MunicipioNotificacionNal')
    telefono_celular_empresa = models.CharField(max_length=15, blank=True, null=True, db_column='T010telCelularEmpresa')
    telefono_empresa_2 =models.CharField(max_length=15, null=True, blank=True, db_column='T010telEmpresa2')
    cod_pais_nacionalidad_empresa = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T010Cod_PaisNacionalidadDeEmpresa')
    acepta_notificacion_sms = models.BooleanField(default=False, db_column='T010AceptaNotificacionSMS')
    acepta_notificacion_email = models.BooleanField(default=False, db_column='T010AceptaNotificacionEmail')
    acepta_tratamiento_datos = models.BooleanField(default=False, db_column='T010AceptaTratamientoDeDatos')
    
    def __str__(self):
        return str(self.id_persona)
    
    class Meta:
        db_table = 'T010Personas'
        verbose_name='Persona'
        verbose_name_plural='Personas'
        
class HistoricoDireccion(models.Model):
    
    class tipo_direccion_CHOICES(models.TextChoices):
        Laboral = "L", "Laboral"
        Residencia = "J", "Residencia"
        Notificacion = "N","Notificacion"
        
    id_historico_direccion = models.AutoField(primary_key=True, editable=False, db_column='T015IdHistoDireccion')
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column = 'T015Id_Persona')    
    direccion = models.CharField(max_length=255, db_column='T015direccion')
    cod_municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T015Cod_MunicipioEnCol')
    cod_pais_exterior = models.CharField(max_length=2, choices=paises_CHOICES,null=True, db_column='T015Cod_PaisEnElExterior')
    tipo_direccion = models.CharField(max_length=1, choices=tipo_direccion_CHOICES.choices,db_column='T015TipoDeDireccion')
    fecha_cambio = models.DateTimeField(auto_now_add=True, db_column='T015fechaCambio')
        
    def __str__(self):
        return str(self.id_historico_direccion)

    class Meta:
        db_table = 'T015HistoricoDirecciones'
        verbose_name='Histórico de dirección '
        verbose_name_plural='Histórico de direcciones'
        
class ApoderadoPersona (models.Model):
    persona_poderdante = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T013IdPersonaPoderdante')
    id_proceso = models.CharField(max_length=50, db_column = 'T013IdProceso') #Pendiente por foreingKey de tabla procesos
    consecutivo_del_proceso = models.AutoField(primary_key=True, editable=False, db_column = 'T013ConsecDelProceso') #Pendiente por foreingKey de tabla procesos
    persona_apoderada = models.ForeignKey(Personas, on_delete=models.CASCADE,  related_name='persona_apoderada', db_column = 'T013IdPersonaApoderada')
    fecha_inicio = models.DateTimeField(db_column = 'T013fechaInicio')
    fecha_cierre = models.DateTimeField(db_column = 'T013fechaCierre', null=True, blank=True)
    
    def __str__(self):
        return str(self.persona_poderdante)

    class Meta:
        db_table = 'T013Apoderados_Persona'    
        verbose_name='Apoderado'
        verbose_name_plural='Apoderados'
           
class HistoricoEmails(models.Model):
    id_histo_email = models.AutoField(primary_key=True, db_column='T016IdHistoEmail')
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T016Id_Persona')
    email_notificacion = models.EmailField(max_length=100, db_column='T016emailDeNotificacion')
    fecha_cambio = models.DateTimeField(auto_now=True, db_column='T016fechaCambio')

    def __str__(self):
        return self.email_notificacion

    class Meta:
        db_table = 'T016HistoricoEmails'      
        verbose_name='Historico de email'
        verbose_name_plural='Históricos de email'
        
class SucursalesEmpresas(models.Model):
    id_empresa = models.ForeignKey(Personas,on_delete=models.CASCADE,  db_column='T012IdEmpresa')#Es primary_key????
    numero_sucursal = models.AutoField(primary_key=True, editable=False, db_column='T012NroSucursal')
    sucursal = models.CharField(max_length=255, db_column='T012sucursal')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, db_column='T012codMunicipio')
    direccion = models.CharField(max_length=255, db_column='T012direccion')
    direccion_sucursal_georeferenciada = models.CharField(max_length=50, db_column='T012ubicacionGeoreferenciada') ##Foreing_Key con tabla persoas??
    pais_sucursal_exterior = models.CharField(max_length=2, choices=paises_CHOICES, db_column='T012cod_sucursal_exterior')
    direccion_correspondencias = models.CharField(max_length=50, db_column='T012direccionCorrespondencias')
    email_sucursal = models.EmailField(max_length=255, db_column='T012emailSucursal')
    telefono_sucursal = models.CharField(max_length=10, db_column='T012telContactoSucursal')
    es_principal = models.BooleanField(default=False, db_column='T012esPrincipal')
    
    def __str__(self):
        return self.sucursal
    
    class Meta:
        db_table = 'T012SucursalesEempresa'
        verbose_name='Sucursal'
        verbose_name_plural='Sucursales'
        
class User(AbstractBaseUser,PermissionsMixin):
    
    class tipo_usuario_CHOICES(models.TextChoices):
        interno="I","Interno"
        externo="E","Externo"
        
    id_usuario = models.AutoField(primary_key=True, editable=False, db_column='TzIdUsuario')
    nombre_de_usuario = models.CharField(max_length=30, db_column='TznombreUsuario')
    persona = models.OneToOneField(Personas, on_delete=models.SET_NULL, null=True,db_column='TzId_Persona')
    is_active = models.BooleanField(max_length=1, default=False, db_column='Tzactivo')
    is_staff = models.BooleanField(default=False, db_column='Tzstaff')#Añadido por Juan
    is_superuser = models.BooleanField(default=False, db_column='TzsuperUser')  #Añadido por Juan
    is_blocked = models.BooleanField(max_length=1,default=False, db_column='Tzbloqueado')
    id_usuario_creador = models.ForeignKey('self', on_delete=models.SET_NULL,null=True, db_column="TzId_Usuario_Creador")
    created_at = models.DateTimeField(auto_now_add=True, db_column='TzfechaCreacion')
    activated_at = models.DateTimeField(null=True, db_column='TzfechaActivacionInicial')
    tipo_usuario = models.CharField(max_length=1,null=True, choices=tipo_usuario_CHOICES.choices, db_column='TztipoUsuario') #Juan Camilo Text Choices
    email = models.EmailField( unique=True, db_column='TzemailUsuario') #Añadido por Juan
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)
    
    class Meta:
        db_table = 'TzUsuarios'
        verbose_name='Usuario'
        verbose_name_plural='Usuarios'

class UsuariosRol(models.Model):
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True, db_column='TzIdRol')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_column='TzIdUsuario')

    class Meta:
        db_table='TzUsuarios_Rol'
        verbose_name='Rol de usuario'
        verbose_name_plural='Roles de usuario'

class Auditorias(models.Model):
    
    class subsistema_CHOICES(models.TextChoices):
        Almacen="ALMA","Almacen"
        Conservacion="CONS","Conservación"
        Gestion_Documental="GEST","Gestión Documental"
        Recurso_hidrico="RECU","Recurso Hídrico"
        tramites_servicios="TRAM","Trámites y servicios"
        Seguimiento_planes="PLAN","Seguimiento a planes"
        Recaudo="RECA","Recaudo"
        
    id_auditoria=models.AutoField(db_column='TzIdAuditoria',primary_key=True, editable=False)
    id_usuario=models.ForeignKey(User, on_delete=models.CASCADE, db_column='TzId_Usuario') ##No tiene definido tipo de relacion
    id_modulo=models.ForeignKey(Modulos, on_delete=models.CASCADE, db_column='TzId_Modulo')
    id_cod_operacion=models.ForeignKey(Permisos, on_delete=models.CASCADE, db_column='TzCod_Operacion')
    fecha_accion=models.DateField(db_column='TzfechaAccion')
    subsistema=models.CharField(max_length=4,choices=subsistema_CHOICES.choices, db_column='Tzsubsistema') #Juan camilo text choices
    dirip=models.CharField(max_length=255,db_column='Tzdirip')
    descripcion=models.TextField(db_column='Tzdescripcion')
    valores_actualizados=models.CharField(max_length=255, null=True, blank=True, db_column='TzvaloresActualizado')
    
    class Meta: 
        db_table ='TzAuditorias'
        verbose_name='Auditoría'
        verbose_name_plural='Auditorías'
        
    def __str__(self):
         return str(self.id_auditoria)   
      
class HistoricoActivacion(models.Model):
    class OperacionesSobreUsuario(models.TextChoices):
        Activar = "A", "Activar"
        Desactivar = "D", "Desactivar"
        Bloquear = "B", "Bloquear"
        Unlock = "U", "Unlock"

    id_historico = models.AutoField(primary_key=True, editable=False, db_column='T014IdHistorico')
    id_usuario_afectado = models.ForeignKey(User, on_delete=models.CASCADE, db_column='T014Id_Usuario_Afectado')
    cod_operacion = models.CharField(max_length=1, choices=OperacionesSobreUsuario.choices, db_column='T014Cod_Operacion')
    fecha_operacion = models.DateTimeField(auto_now = True, db_column='T014fechaOperacion')
    justificacion = models.TextField( db_column='T014justificacion')
    usuario_operador = models.ForeignKey(User, related_name='usuarioOperador',on_delete=models.CASCADE, db_column='T014usuarioOperador')  #Añadido por Juan

    def __str__(self):
        return self.fecha_operacion

    class Meta:
        db_table = 'T014HistoricoActivacion'  
        verbose_name='Histórico de activación'
        verbose_name_plural='Histórico de activaciones'

class ClasesTercero(models.Model):
    id_clase_tercero = models.AutoField(primary_key=True, editable=False, db_column='T007IdClaseTercero')
    nombre = models.CharField(max_length=30, db_column='T007nombre')
    
    def __str__(self):
        return str(self.id_clase_tercero)

    class Meta:
        db_table='T007ClasesTercero'
        verbose_name='Clase tercero'
        verbose_name_plural='Clase terceros'

class ClasesTerceroPersona(models.Model):
    id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE, db_column='T011IdClaseTercero')
    id_clase_tercero = models.ForeignKey(ClasesTercero, on_delete=models.CASCADE, db_column='T011IdPersona')
    class Meta:
        db_table='T011ClasesTercero_Persona'
        verbose_name='Clase tercero persona'
        verbose_name_plural='Clase tercero personas'

