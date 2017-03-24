<?xml version="1.0" encoding="UTF-8"?>
<!-- 
   This file is a part of the source code and related artifacts for the
   Project Bamboo 
   
   For more information please see:
   http://www.projectbamboo.org
   https://wiki.projectbamboo.org
    
   Copyright 2012 
   The Regents of the University of California, Berkeley ("Berkeley") 
   the Australian National University; Indiana University 
   Northwestern University 
   Tufts University
   University of Chicago
   The Board of Trustees of the University of Illinois at Urbana-Champaign 
   University of Maryland 
   University of Oxford
   University of Wisconsin, Madison 
  
   Licensed under the Educational Community License (ECL), Version 2.0.
   You may not use this file except in compliance with this License.
   You may obtain a copy of the ECL 2.0 License at:
   https://source.projectbamboo.org/svn/btp/LICENSE.txt
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
   Based on code from The Alpheios Project  
   Copyright 2008-2009 Cantus Foundation
   http://alpheios.net
   published under the GNU General Public License
   http://www.gnu.org/licenses/
 -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0"
	    xmlns:exsl="http://exslt.org/common"
	    xmlns:ri = "http://chs.harvard.edu/xmlns/refindex/1.0"
	    xmlns:cs = "http://shot.holycross.edu/xmlns/citequery"
	    xmlns:sparql = "http://www.w3.org/2005/sparql-results#">
    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>
    <xsl:strip-space elements="*"/>
		    
  <xsl:param name="e_lexicalEntitySvc"/>
  <xsl:param name="e_lexicalEntityBaseUri" select="'http://data.perseus.org/collections/'"/>
  <xsl:param name="e_stripSense" select="false()"/>
 
  <xsl:template match="@*|node()">        
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  
    <xsl:template match="entry">
      <xsl:variable name="lemma" select="dict[1]/hdwd[1]"/>
      <xsl:variable name="uri">
      	<xsl:if test="$e_lexicalEntitySvc">
      		<xsl:copy-of select="document(concat($e_lexicalEntitySvc,escape-html-uri($lemma)))"/>
      	</xsl:if>
      </xsl:variable>
      <xsl:variable name="uris">
      	<xsl:choose>
      		<!--  for backwards compatibility support CITE CS reply -->
	        <xsl:when test="$uri//cs:reply//cs:citeObject[@urn]">
	          <xsl:value-of select="$uri//cs:reply/cs:citeObject/@urn"/>
	        </xsl:when>
	        <!-- default is a sparql query that returns one or more URIs -->
      	  <!-- may return redirect urns in replacedby binding - if so use that --> 
	        <xsl:otherwise>
	          <xsl:choose>
	            <xsl:when test="$uri//sparql:results/sparql:result/sparql:binding[@name='replacedby']/sparql:uri">
	              <xsl:value-of select="$uri//sparql:results/sparql:result/sparql:binding[@name='replacedby']/sparql:uri"/>
	            </xsl:when>
	            <xsl:otherwise>
	              <xsl:value-of select="$uri//sparql:results/sparql:result/sparql:binding[@name='urn']/sparql:uri"/>
	            </xsl:otherwise>
	          </xsl:choose>
	        </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:element name="entry">
        <xsl:if test="$uris != ''">
          <xsl:attribute name="uri" select="string-join(concat($e_lexicalEntityBaseUri,$uris),' ')"/>
        </xsl:if>
        <xsl:apply-templates select="@*"/>
        <xsl:apply-templates select="node()"/>
      </xsl:element>
    </xsl:template>
  
</xsl:stylesheet>
