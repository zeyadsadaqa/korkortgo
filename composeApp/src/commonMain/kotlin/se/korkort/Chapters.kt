package se.korkort

data class Chapter(val title: String, val category: Category, val page: Int, val endPage: Int, val summary: String)
val chapters = listOf(
Chapter("The foundations",Category.RULES,6,12,"""Traffic safety is a shared responsibility. Show consideration, avoid unnecessary obstruction and give particular care to children, older people and people with disabilities. Communicate intentions early and keep room for errors.

Police directions take precedence over signals, then signs, then general rules. A green light does not remove obligations to avoid a blocked junction or protect people crossing a road you turn into.

Adapt speed to visibility, grip, the load, the vehicle and the traffic. You must be able to stop within the road you can see and before foreseeable obstacles. A posted limit is a maximum, not a target. The general basic limits are 50 km/h in built-up areas and 70 km/h outside them, unless other limits apply."""),
Chapter("Lanes & positioning",Category.RULES,14,20,"""A lane can exist without painted lines if there is sufficient width for a normal file of four-wheeled vehicles. Normally use the rightmost lane. With at least two marked lanes in your direction and a limit of 70 km/h or less, or destination-specific lanes, you may choose the lane most suitable for your route.

Keep a position that leaves safe margins to oncoming traffic, parked cars and the edge. Before a right turn move appropriately towards the right edge; before a left turn position towards the centre without obstructing oncoming traffic. On a one-way road, a left turn is prepared from the left.

Before changing lanes check ahead, mirrors and blind spot, signal, judge others' reactions, check again and move smoothly. A signal does not grant priority. Do not weave between lanes to jump a queue. Respect solid lines and reserved lanes. A right-side public-transport lane may also be used by bicycles and class II mopeds; other exceptions are shown on panels."""),
Chapter("Priority & junctions",Category.RULES,22,44,"""Give way clearly and early; stop if needed. At a stop sign make a complete stop at the line, or before the intersecting road when no line exists. Every driver must make their own stop.

Without another priority arrangement, give way to vehicles from the right. This can apply at T-junctions and in open areas. Neither a wider road nor travelling straight ahead automatically gives priority. A priority-road sign identifies a road whose joining traffic must yield; remain alert for mistakes.

When leaving a property, petrol station, parking area, pedestrian street, home zone or bicycle street, the exit rule requires you to yield to traffic whose path you cross. Crossing an uninterrupted footpath or cycle path is also relevant. A raised crossing is not automatically an uninterrupted path: assess the actual design and signs.

Left turns must not obstruct oncoming traffic. Turning also requires consideration for people crossing the road you enter. Keep junctions and crossings clear. At limits of 50 km/h or less, allow a signalling bus to leave its stop into the affected rightmost lane. Make room for emergency vehicles without creating another hazard.

Red means stop, and red with amber still means stop. Amber requires stopping unless you are too close to stop safely. Flashing amber requires caution and the applicable signs or ordinary priority rules. A round green signal may coexist with a green for opposing traffic."""),
Chapter("Pedestrians & cyclists",Category.RULES,46,56,"""At an uncontrolled pedestrian crossing, give way to people already crossing or about to enter. A person pushing a bicycle is a pedestrian. A cyclist riding over a pedestrian crossing does not acquire pedestrian priority. Never assume a person has seen you, and avoid waving them across other traffic lanes.

At an uncontrolled bicycle passage, adapt speed to avoid endangering cyclists on it. A cyclist entering from a cycle path normally has a duty to yield. If you turn across the passage or cross it while exiting a roundabout, travel slowly and let cyclists on or about to enter it pass.

A bicycle crossing is identified by the appropriate sign and markings and has traffic-calming design. Drivers give way to cyclists and class II moped riders on or about to use it. Riders must still consider approaching traffic.

A controlled crossing has operating signals or police control. People who entered lawfully may need time to finish even after their signal changes. When crossing an uninterrupted footpath or cycle path, give way to its users."""),
Chapter("Roundabouts",Category.RULES,58,66,"""Circulate anticlockwise around the central island and yield to vehicles already circulating. Plan your lane from signs, markings and your exit. Changing lanes inside the roundabout requires the same observation and care as elsewhere.

Indicate right when leaving. Indicate lane changes; do not use a signal as a claim of priority. There is no special general requirement to indicate left on entry. Any additional signal should help others understand you rather than suggest an unintended lane change.

If you cannot cross the outer lane safely, continue around rather than cutting across another vehicle. At an exit, check pedestrians and cyclists as carefully as at any other turn."""),
Chapter("Stopping & parking",Category.RULES,68,76,"""Waiting for traffic or avoiding danger is different from voluntary stopping. Actual boarding, alighting, loading and unloading are not parking. Waiting for someone who has not yet arrived is normally parking even with the engine running.

Do not voluntarily stop in a tunnel, junction, roundabout, bicycle lane, public-transport lane or where you hide a sign or create danger. Keep 10 metres clear before pedestrian and bicycle crossings and relevant paths; keep the required clearance at junctions. Where a solid centre line is on your side, a stopped car generally needs at least 3 metres to that line.

Parking is prohibited within 30 metres of a railway crossing, on a priority road unless permitted, across an entrance, at a passing place, or outside a marked space's boundaries. Normally stop or park on the right; either side can be used on a one-way street if otherwise allowed.

Read signs and supplementary panels together. Parenthesised times apply on weekdays before Sundays and public holidays; red times denote Sundays and public holidays. A named day applies even if that day is a holiday. Under date parking, the prohibited house-number side has the same odd/even parity as the date during the stated hours.

Set a parking disc to the next half-hour after arrival while the requirement applies. At an unmarked bus stop the protected area is 20 metres before and 5 metres after the sign. Boarding or alighting is allowed only without hindering public transport; goods loading is not that exception.

Secure the vehicle against rolling and unauthorised use. Consider wheel direction on slopes. Never leave children or animals in a dangerously hot car."""),
Chapter("Country roads",Category.SAFETY,78,88,"""Higher speeds demand longer sight lines and safety margins. Look well ahead and signal turns early. A left turn across fast traffic combines crossing and rear-impact risks. If the turn is unsafe, consider a safer route or a suitable turning place farther on. Keep wheels straight while waiting.

Use a time gap, such as the three-second guideline in favourable conditions, and increase it for poor grip or visibility. If someone follows too closely, create more space ahead so you can slow gradually. Let the driver pass at a suitable safe place.

On narrow roads cooperate at passing places. If an obstacle is on your side, allow oncoming traffic through when needed. Pass horses slowly, quietly and with space. At roadworks follow temporary arrangements and protect exposed workers.

A private road is not automatically subordinate to a public road: normal priority rules or the exit rule depend on the situation. Verge posts help show alignment; yellow reflectors may indicate a junction or access. A dashed route-number border indicates a route leading towards that numbered road."""),
Chapter("Motorways & clearways",Category.RULES,90,96,"""Motorways separate opposing traffic and have no at-grade intersections. Clearways also exclude at-grade crossing traffic but may have opposing traffic. A central barrier alone does not prove the road is a motorway or clearway: look for its sign.

Use the acceleration lane to match speed, observe and cooperate. If there is no acceleration lane, entering traffic yields. Do not reverse, turn around, walk, cycle, drive a moped or make a voluntary stop on a motorway or clearway. If you miss an exit, continue to the next suitable one.

Prepare early for your exit and brake appropriately in the deceleration lane. After long high-speed driving, check the speedometer: subjective speed can feel deceptively low. Monotony, close following and standing water remain hazards on otherwise safe roads."""),
Chapter("Overtaking",Category.SAFETY,98,106,"""An overtake needs enough visible unobstructed road for the whole manoeuvre and a safe return. Check for someone already overtaking you, signal, keep lateral clearance and stay within the speed limit.

Normally pass on the left. Specific situations permit right-side passing, such as a vehicle turning left, certain marked multilane roads at limits no higher than 70 km/h, destination-separated lanes or queues. These exceptions do not remove the duty to avoid danger.

Do not overtake into obscured visibility or immediately before or on an uncontrolled pedestrian crossing. Junctions and unprotected railway crossings have additional restrictions. If someone overtakes you, do not accelerate or obstruct them, even if their action is unlawful.

The time saving from a higher speed is often small compared with the extra risk. Distinguish what is technically permitted from what is sensible in the actual visibility and traffic."""),
Chapter("Railway crossings",Category.SAFETY,108,114,"""Trains cannot swerve and may need a very long distance to stop. Always check and yield to a train, even without a flashing warning. A white crossing light is not a guarantee that no train is approaching.

Approach at a speed suited to visibility and cross only when the whole vehicle can reach clear space beyond the tracks. Do not queue on the crossing. Use a suitable gear and avoid unnecessary gear changes while on the rails.

If trapped, get people away from the tracks and alert 112. If a vehicle can be moved safely, barriers are designed to give way rather than trap it. Do not take personal risks trying to save property.

The three-, two- and one-bar approach signs show decreasing distance. The presence of barriers or normal red/amber/green signals affects overtaking restrictions, but never removes the need for a safe manoeuvre."""),
Chapter("Special streets",Category.RULES,116,122,"""In a home zone, travel at walking speed, yield to pedestrians and park only where designated. These duties remain even when the street appears empty.

A pedestrian street permits only specified motor access, such as certain deliveries, access to residences and hotels, or transport of sick or mobility-impaired people. Walking-speed and pedestrian-priority requirements apply when access is permitted.

On a bicycle street, do not exceed 30 km/h and adapt to cyclists. Yield when entering and when leaving for another road, and use designated parking places.

A recommended lower speed is different from a mandatory speed-limit sign, but you must still choose a speed that is safe for the conditions."""),
Chapter("Winter & changing grip",Category.SAFETY,124,130,"""The most deceptive conditions are often local icy patches rather than obvious deep snow. Bridges, shaded areas and compressed snow at junctions deserve attention. A wet-looking surface with little tyre spray may be frozen. Ice can occur when the air temperature is a few degrees above zero.

Freezing rain can create an almost invisible ice layer. Snow smoke reduces sight distance; increase the gap and avoid entering a cloud at speed. Tracks in snow may have different grip from the surrounding slush. Snowplough width does not always equal usable road width: use roadside markers carefully.

Carry warm clothing, suitable footwear, a charged phone, scraper, visibility equipment and appropriate recovery supplies for the trip. Clear snow and ice from the vehicle before driving.

Grip also changes in other seasons. Wet leaves, mud from farm vehicles, heat-softened surfaces and the first rain after a dry spell can all be slippery."""),
Chapter("Learning & judgement",Category.PERSONAL,132,138,"""Learn the reasons behind rules rather than answer letters. Repeated practice with vehicle controls frees attention for traffic. Copy good habits critically: confidence and experience do not make every role model safe.

A mature driver accepts errors, cooperates and avoids using traffic to express frustration. Overconfidence can develop before experience is broad enough to recognise rare hazards. Familiarity should guide anticipation without becoming complacency.

Allow time, prepare the route and vehicle, and avoid rushing. Excessive stress can produce tunnel vision and poor decisions. Passengers can reduce risk by supporting safe choices and speaking calmly when driving becomes unsafe."""),
Chapter("Alcohol, medication & distraction",Category.PERSONAL,140,146,"""Sweden's numerical drink-driving threshold is 0.2 per mille in blood or 0.1 mg/l in breath. The numerical aggravated threshold is 1.0 per mille or 0.5 mg/l; other circumstances can also make an offence serious. Do not use a threshold as a target for safe drinking before driving.

Coffee, showers and exercise do not provide a reliable shortcut to eliminate alcohol. The following day, both residual alcohol and fatigue can affect fitness. Drug use can impair judgement, coordination and perception. A prescription does not authorise driving while impaired; check the leaflet and professional advice.

Do not use handheld communication equipment while driving. Hands-free conversations and built-in screens can still distract. Set navigation before departure or stop somewhere safe and permitted to make complex changes."""),
Chapter("Fatigue",Category.PERSONAL,148,152,"""Sleep deprivation affects attention, coordination, decisions and reaction. Monotonous roads can make it harder to remain alert. Warning signs include repeated yawning, heavy eyelids, drifting position and difficulty maintaining speed.

A microsleep is an involuntary loss of wakefulness, even if very brief. Stop safely before fatigue reaches that point. Adequate sleep is the fundamental remedy; fresh air, music or willpower do not replace it. A break or nap may help temporarily, but continue only when fit to drive.

Plan rest and avoid assuming that being close to your destination makes continued driving safe. Driving can be prohibited when fatigue makes you incapable of safe control."""),
Chapter("Vision & perception",Category.PERSONAL,154,160,"""Central vision provides fine detail; peripheral vision helps notice movement outside your direct focus. Scan actively across near and far areas rather than staring at one object. Experience should help you identify likely hazards without making you ignore unexpected ones.

Stress, tiredness and alcohol can narrow attention. At night a vehicle with one failed headlamp may be mistaken for a narrow motorcycle. Snow spray and unusual lighting can also mislead perception.

Use prescribed corrective lenses and keep windows and lights clean. Hearing, balance, touch and smell also provide information, such as a siren, unusual vibration or signs of leakage."""),
Chapter("Sharing the road with disabilities",Category.SAFETY,162,166,"""A disability may be visible or hidden. Allow time and avoid interpreting slow movement as deliberate obstruction. A white cane may indicate impaired vision, while hearing impairment may mean a person cannot hear your approach.

Stop clearly and early for a visually impaired pedestrian and avoid revving or unnecessary horn use. Let the person complete the crossing without confusing changes in engine sound. Do not distract a working guide dog.

Older people may need more time to perceive, decide and move. Adapt to the individual situation rather than relying on assumptions about a person's abilities."""),
Chapter("Children in traffic",Category.SAFETY,168,172,"""Children are small enough to be hidden by parked vehicles and may act impulsively. Their ability to judge speed, locate sound and predict risk is still developing. Eye contact does not guarantee they will wait.

Slow down around schools, play areas and stopped school buses. Look for movement between vehicles and leave room for the unexpected. Crossing guards draw attention to children but do not have the same legal powers as police directing traffic.

Children are also particularly vulnerable to poor air quality. Thoughtful route, speed and vehicle choices help protect them both inside and outside the car."""),
Chapter("Collisions & emergency response",Category.SAFETY,174,186,"""At a collision, first assess danger and prevent further harm. Call 112 for an emergency and give the location, hazards and what you know about casualties. Follow the operator's instructions. Do not expose yourself to traffic or dangerous substances.

If involved, stop and exchange the necessary details. For damage to unattended property, try to reach the owner and notify police if you cannot. Keep witnesses' and vehicles' details for the insurer. Avoid moving evidence after a serious collision unless required for safety.

Warn others appropriately after a breakdown. Position a warning triangle to give approaching traffic useful notice when required, without putting yourself at risk. Keep away from a damaged dangerous-goods vehicle and report its markings from a safe distance.

After hitting a reportable species such as roe deer, mark the location safely and notify police even if the animal runs away. Do not chase it. Look especially carefully near fence ends, fields and water at dusk and dawn.

Vision Zero aims to prevent deaths and serious injuries through safer roads, vehicles and behaviour, while recognising that people make mistakes."""),
Chapter("Vehicle types",Category.VEHICLE,188,194,"""Road users include drivers, riders, cyclists and pedestrians. Vehicles are not limited to motor vehicles: bicycles and horse-drawn vehicles also count. Rail-bound transport has separate treatment.

A normal passenger car or light lorry without a trailer generally follows the road's speed limit, with safe adaptation. Other vehicles can have lower vehicle-specific limits. A heavy lorry without a trailer has a 90 km/h maximum on motorways and clearways and 80 km/h elsewhere, subject to lower posted limits.

A class I moped is limited to 45 km/h but is still prohibited on motorways. When towing, check both the combination's technical and licence limits and its permitted speed; do not infer them from the road sign alone."""),
Chapter("Reaction, braking & stopping",Category.SAFETY,196,202,"""Reaction distance is movement between detecting a hazard and beginning your response. At a fixed reaction time it grows directly with speed. Convert km/h to m/s by dividing by 3.6, then multiply by reaction time.

Braking distance begins when braking starts. Under an unchanged simple model it grows with speed squared: double speed means about four times the braking distance. Real grip, slope, tyres, brakes and load affect the result.

Stopping distance is reaction plus braking distance. The book's rough dry-road estimate uses (speed ÷ 10) × reaction time × 3 for reaction distance and (speed ÷ 10)² × 0.4 for braking. These are learning estimates, not guaranteed performance.

Anticipation can reduce delay. Worn tyres do not directly change the driver's reaction time, but can substantially worsen the braking phase."""),
Chapter("Tyres",Category.VEHICLE,204,212,"""Tyres must suit the vehicle and conditions. For a normal light passenger car, the summer-use minimum tread depth is 1.6 mm. During 1 December–31 March in winter road conditions, the winter requirement is at least 3 mm. Winter conditions include snow, ice, slush or frost.

Studded tyres are generally allowed 1 October–15 April and outside that interval when winter conditions prevail or are expected. Local studded-tyre prohibitions can also apply. Check current requirements for approved non-studded winter tyres and any trailer you tow.

Use the recommended pressures for the load. Watch for damage, uneven wear and vibration. Fit the best grip at the rear to reduce rear breakaway. Wheel imbalance can cause vibration; alignment faults can cause pulling and uneven wear.

A temporary spare or repair kit has limitations: follow the car's instructions and arrange a proper repair. With a studded car in winter conditions, the trailer must also have studded tyres. A trailer's grip is crucial to prevent jack-knifing."""),
Chapter("Steering & stability",Category.VEHICLE,214,222,"""Oversteer means the rear loses grip and the car turns more than intended. Understeer means insufficient front grip makes it turn less than intended. Speed, tyre condition, load, acceleration and braking influence both.

Electronic stability control can apply individual brakes and adjust power to help stabilise the car. It supports the driver but cannot create grip where none exists. Keep it enabled in normal driving and follow vehicle guidance.

Aquaplaning occurs when water prevents proper tyre-road contact. Standing water, speed and worn tread increase risk. Ease off smoothly and avoid abrupt steering or braking if it occurs. Slush can cause a similar loss of contact."""),
Chapter("Brakes",Category.VEHICLE,224,230,"""A dual-circuit braking system retains some braking if one circuit fails. Hydraulic fluid transmits pressure to the brakes. Disc and drum designs achieve friction differently, but both need proper maintenance.

ABS prevents sustained wheel lock and helps retain steering control during hard braking. Pedal pulsation can be normal during ABS operation: maintain firm pressure rather than pumping. ABS does not guarantee a shorter distance on every surface.

A sinking or unusually spongy pedal, pulling under braking, leakage or warning lights need investigation. Check braking cautiously after washing or driving through water. Follow the vehicle's service schedule for brake fluid and components.

The parking brake secures the vehicle when parked. Use the appropriate gear or transmission position and consider slope and kerb direction as additional protection."""),
Chapter("Crash protection",Category.SAFETY,232,236,"""Crumple zones absorb energy while the passenger cell preserves occupied space. A seat belt restrains you during the crash and works together with the airbags. Tighten the belt close to the body and route it correctly; bulky clothing can impair fit.

Adjust the head restraint and sit close to the seat back to reduce damaging neck movement, particularly in a rear impact. An airbag is not a substitute for a belt, and sitting too close can cause injury.

The driver must ensure that passengers under 15 use the required protection. Protect every occupant and secure luggage as well: loose objects can become projectiles."""),
Chapter("Child restraints",Category.SAFETY,238,242,"""Children shorter than 135 cm normally require an appropriate approved restraint. Choose one that fits the child and the vehicle and follow its height, weight and installation instructions. Limited exceptions for short occasional journeys do not replace proper planning.

Young children are best protected rear-facing for as long as the approved seat permits. Their head and neck need more support than an adult's. Do not put a rear-facing child seat in front of an active frontal passenger airbag.

Transportstyrelsen also advises against putting children in child seats or boosters at a passenger position with an active frontal airbag, and gives 140 cm as its general height guidance. Follow the official guidance and the vehicle and restraint manufacturers' instructions.

Check belt routing and tightness each trip. An adult's arms cannot substitute for a child restraint in a collision."""),
Chapter("Dimensions & projecting loads",Category.VEHICLE,244,250,"""For ordinary loads under the general rule, consider both lateral projection and overall width: the book describes a 20 cm side-projection limit and 2.6 m overall width. Special indivisible-load rules and exemptions are separate; do not assume the ordinary rule authorises exceptional transport.

Projecting loads need visible marking. A rear projection exceeding 1 metre must be marked. A forward projection also needs marking unless the short clearly visible exception applies. In darkness, use the required lights and reflectors: white forwards, red rearwards.

When towing another vehicle, mark a tow connection if the gap exceeds 2 metres. Trailer reflectors and lights have prescribed colours and positions; check that nothing obscures them."""),
Chapter("Loads & trailers",Category.VEHICLE,252,260,"""Secure everything against forward, rearward and sideways movement. Place heavy cargo low and against suitable supports, use rated securing points and straps, and keep loose objects off the parcel shelf. Roof loads affect stability and must include the rack or box within the car's allowed roof weight.

Unladen weight describes the vehicle in its standard unloaded configuration including the defined driver allowance. Registered total weight is unladen weight plus maximum permitted load. Gross weight is what it actually weighs at a given time.

Ordinary B covers a car up to 3,500 kg total weight with a trailer up to 750 kg total weight. A trailer over 750 kg can also qualify when combined registered total weights do not exceed 3,500 kg. Always respect the car's separate technical towing and combination limits. B96 or BE changes licence entitlement, not the car's engineering limits.

Load the trailer for its specified towball pressure. Too much or too little coupling load can impair the towing car's grip and stability. Check coupling, safety connection, tyres, lights, brakes and secure load before departure."""),
Chapter("Lights & signals",Category.VEHICLE,262,270,"""Use the correct lighting both to see and to be seen. In suitable daylight, approved daytime running lights can be used instead of dipped headlights. Some cars leave rear lights off in that mode: select the required lighting manually when darkness, twilight or poor weather demands it.

Do not combine dipped headlights with front fog lights or daytime running lights. Full beam is useful on dark roads but must not dazzle oncoming drivers, a driver ahead or other affected traffic. Heavy fog or snow can reflect high beams back and worsen your view.

Use rear fog lights only when reduced visibility requires them, and avoid dazzling a following driver unnecessarily. Parking lights make a stationary car visible in appropriate conditions. Brake, reverse, number-plate and trailer lights also need checking.

Signal turns, lane changes and other significant sideways movements. Continue observing after signalling: an indicator does not grant priority."""),
Chapter("Before you drive",Category.VEHICLE,272,276,"""Check the condition of tyres, exterior lights, reflectors, windows and registration plates. Check brake lights with help or a suitable reflection. Make sure the load is secure and doors are closed.

Adjust the seat, head restraint, belt and mirrors before moving. Check that the brakes feel normal and that steering assistance and required warning-lamp checks behave as the manufacturer describes. Know how to use the demisters, wipers and lights without prolonged searching.

Do not treat a quick walk-around as a substitute for scheduled maintenance, and do not drive with a serious safety defect."""),
Chapter("Inspections",Category.VEHICLE,278,282,"""Periodic inspections check roadworthiness and relevant environmental requirements. For an ordinary car no heavier than 3,500 kg, the first deadline is 36 months after the month it entered service, the second 24 months after the month of the first inspection, then 14 months after the month of the previous inspection.

The owner must meet the deadline even without a reminder. Missing it normally creates an automatic driving ban. Follow the requirements for correcting defects and any reinspection. A driving ban is different from registered off-road status.

Police or vehicle inspectors can conduct roadside checks. Substantial modifications may require a registration inspection rather than only the ordinary periodic check."""),
Chapter("Maintenance essentials",Category.VEHICLE,284,288,"""The battery stores electrical energy; conventional vehicles recharge it through their charging system. Battery chemicals can be corrosive. Follow the correct procedure for the vehicle rather than improvising connections or servicing a sealed battery.

Fuses protect circuits against excessive current. Replace only with the specified type and investigate recurring failures. Never bypass the protection.

Coolant controls engine temperature, and engine oil lubricates moving parts. Do not open a hot pressurised cooling system. Check levels as the manufacturer directs and respond promptly to oil-pressure or overheating warnings.

Keep sufficient suitable washer fluid, particularly in winter. Clear visibility is a safety requirement, not merely a convenience."""),
Chapter("Registration & ownership",Category.VEHICLE,290,296,"""Registration information identifies the vehicle's technical data, ownership and status. Part 1 contains technical details; Part 2 is used for ownership-related procedures and should be kept securely.

When ownership changes, verify details and arrange the required insurance from the relevant date. Use Transportstyrelsen's current services or the prescribed paperwork.

Off-road status requires an active notification. It does not happen automatically because a car is unused or has a driving ban. Only limited permitted journeys may be made with an off-road vehicle under specific conditions; check official requirements before moving it."""),
Chapter("Insurance",Category.VEHICLE,298,302,"""Compulsory third-party insurance primarily covers personal injury and damage to other people's property. It does not provide own-car damage cover merely because it is your policy.

Partial and comprehensive policies add protection, with terms that vary by insurer. Understand the exclusions, excess, assistance provisions and any cover for own-vehicle damage rather than assuming every policy is identical.

Keep the information needed after an incident: date, location, vehicles, people, witnesses and damage. Serious misconduct can affect the insurer's ability to recover costs from the responsible person."""),
Chapter("Environment & health",Category.ENVIRONMENT,304,310,"""Burning fossil fuel adds carbon dioxide to the atmosphere and contributes to the enhanced greenhouse effect. Vehicle impacts also include local air pollution, noise, materials and energy used in production.

Catalytic converters reduce several harmful exhaust components once warm, but do not remove fossil carbon dioxide emissions. Carbon monoxide interferes with oxygen transport; nitrogen oxides and hydrocarbons contribute to harmful air chemistry. Exhaust and wear particles affect health.

Remove unnecessary roof equipment and loads, maintain suitable tyre pressure, use energy-consuming equipment sensibly and avoid needless idling. An engine-heater timer can avoid wasting electricity. Wash at a facility that treats polluted runoff.

Lower appropriate speed and smooth driving reduce unnecessary noise. Walking, cycling, public transport or combining trips can avoid car energy use altogether."""),
Chapter("Eco-driving",Category.ENVIRONMENT,312,316,"""Look well ahead and avoid accelerating towards an obvious stop. Smooth planning preserves momentum without compromising priority, crossings or safe gaps. A steady appropriate speed generally uses less energy than repeated acceleration and braking.

In a manual car, leave first gear when appropriate and choose a high enough gear for efficient smooth operation without labouring the engine. Engine braking means releasing the accelerator while a suitable gear remains engaged. Many fuel-injected cars cut fuel during overrun under the right conditions; the exact behaviour depends on the vehicle.

Do not coast with the engine switched off or compromise control to save fuel. If an urgent hazard appears, brake as needed. Safety always takes priority over economy."""),
Chapter("Fuels & environmental zones",Category.ENVIRONMENT,318,322,"""Petrol and diesel contain fossil energy and produce carbon dioxide when burned. Fuel consumption alone does not describe all air-pollution effects. Use only the fuel approved for the vehicle.

An electric vehicle has no tailpipe exhaust while driving, but electricity generation, battery manufacture and tyre and road wear still matter. A hybrid combines an electric motor with a combustion engine; a plug-in hybrid can charge its traction battery externally.

Emission classes identify technical standards. Municipal environmental zones can restrict access according to zone category and vehicle characteristics. Check the current local rule and your vehicle's registered data before entering; a vehicle's appearance or age alone is not sufficient."""),
Chapter("Road signs & markings",Category.RULES,324,360,"""Warning signs identify hazards, priority signs allocate obligations, prohibitory signs restrict actions and mandatory signs specify required directions or routes. Instruction and direction signs help you understand the road and reach your destination.

Read supplementary panels with the main sign. They may define a distance, extent, time, vehicle class or exception. Road markings, signals and police instructions are also part of the traffic system.

Use the official visual catalogue below to study each image and its name. Open its Transportstyrelsen source for the authoritative description and possible variants. Flashing and moving signals cannot be fully understood from a still image alone."""),
Chapter("Lessons from court cases",Category.RULES,362,366,"""The book's cases show why rules must be applied to the complete situation. A driver with nominal priority can still be at fault for excessive speed in poor visibility. Giving way covers conflicting traffic even when another vehicle is badly positioned.

A faulty or incomplete road marking does not automatically cancel the underlying rule. Similarly, staying with the car or leaving the engine on does not turn waiting into active unloading. Unpacking goods inside a shop is different from unloading at the vehicle.

After contact with another vehicle, do not assume that no visible damage removes your duties. Opening a door into a cyclist can also be a traffic-safety offence. Plan for fuel, payment and parking restrictions rather than assuming an inconvenience creates an exemption.

These examples illustrate the book's reasoning. They are not promises of how a future case with different facts will be decided.""")
)
