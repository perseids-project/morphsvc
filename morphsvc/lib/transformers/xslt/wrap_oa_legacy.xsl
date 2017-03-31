<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:oa="http://www.w3.org/ns/oa#"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:cnt="http://www.w3.org/2008/content#"
    xmlns:dcterms="http://purl.org/dc/terms/"
    xmlns:foaf="http://xmlns.com/foaf/0.1/"
    version="1.0">
    
    <!-- this template wraps a treebank annotation in an OA container.
         
         parameters 
            e_datetime - the datetime of the serialization
            e_collection - the urn of the CITE collection which the annotation is/will be a member of
            e_docuri - target of the annotation, if supplied will override anything in the template
    -->
    
    <xsl:param name="e_datetime"/>
    <xsl:param name="e_worduri"/>
    <xsl:param name="e_agenturi"/>
       
    <xsl:output indent="yes"></xsl:output>
    <xsl:strip-space elements="*"/>
    
    <xsl:template match="/">
                
        <xsl:element name="rdf:RDF">
            <xsl:element name="oa:Annotation">
                <xsl:element name="dcterms:creator">
                    <xsl:element name="foaf:Agent">
                        <xsl:attribute name="rdf:about"><xsl:value-of select="$e_agenturi"/></xsl:attribute>
                    </xsl:element>
                </xsl:element>   
                <xsl:element name="dcterms:created">
                    <xsl:value-of select="$e_datetime"/>
                </xsl:element>
                <xsl:element name="oa:hasTarget">
                    <xsl:element name="rdf:Description">
                        <xsl:attribute name="rdf:about"><xsl:value-of select="$e_worduri"/></xsl:attribute>
                    </xsl:element>
                </xsl:element>
                <xsl:apply-templates select="//entry"></xsl:apply-templates>            
            </xsl:element>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="entry">
        <xsl:variable name="bodyid" select="concat('urn:uuid:',generate-id(.))"/>
        <xsl:element name="oa:hasBody">
            <xsl:attribute name="rdf:resource"><xsl:value-of select="$bodyid"/></xsl:attribute>
        </xsl:element>
        <xsl:element name="oa:Body">
            <xsl:attribute name="rdf:about"><xsl:value-of select="$bodyid"/></xsl:attribute>
            <xsl:element name="rdf:type">
                <xsl:attribute name="rdf:resource">cnt:ContentAsXML</xsl:attribute>
            </xsl:element>
            <xsl:element name="cnt:rest">
                <xsl:attribute name="rdf:parseType">Literal</xsl:attribute>
                <xsl:copy-of select="."/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
</xsl:stylesheet>
